import logging
import uuid

from django.db import IntegrityError, transaction as django_transaction
from django.utils import timezone

from apps.account.models import AccountModel
from apps.transaction.email_messages import (
    message_transfer_completed,
    message_recurring_transaction_created,
)
from apps.transaction.models import RecurringTransactionModel, TransactionModel, TransferModel
from apps.transaction.models.choices import TypeTransactionChoices


logger = logging.getLogger(__name__)

class TransactionService:

    # ALTERAÇÕES NO BANCO DE DADOS

    @staticmethod
    @django_transaction.atomic
    def update_balance_account(instance: TransactionModel):
        try:
            account = (
                AccountModel.objects
                .select_for_update()
                .get(id=instance.account_id)
            )

            if instance.processed:
                return

            if instance.type_transaction == 'RECEITA':
                account.balance += instance.value
            else:
                account.balance -= instance.value

            account.save()

            instance.processed = True
            instance.save(update_fields=["processed"])

            return instance

        except IntegrityError:
            # idempotency_key repetida → retorna a transação original
            return TransactionModel.objects.get(
                idempotency_key=instance.idempotency_key
            )

    @staticmethod
    @django_transaction.atomic
    def create_transaction_from_recurring_transaction(instance: RecurringTransactionModel):
        try:
            # bloqueia a conta
            account = AccountModel.objects.select_for_update().get(id=instance.account_id)

            # cria a transação real
            transaction = TransactionModel.objects.create(
                account=account,
                value=instance.value,
                type_transaction=instance.type_transaction,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                recurring_root=instance,
                idempotency_key=uuid.uuid4(),
                processed=True
            )

            TransactionService.update_balance_account(transaction)

            # aplica saldo
            if transaction.type_transaction == 'RECEITA':
                account.balance += transaction.value
            else:
                account.balance -= transaction.value
            account.save()

            # marca a recorrente como processada na primeira execução
            instance.executed_first_time = True
            instance.executed_last_time = timezone.now()
            instance.save()

            django_transaction.on_commit(
                lambda: TransactionService.send_email_when_recurring_transaction_created(
                    instance
                )
            )

            return transaction

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransactionModel.objects.get(idempotency_key=transaction.idempotency_key)

    @staticmethod
    @django_transaction.atomic
    def create_transaction_from_transfer(instance: TransferModel):
        try:
            # bloqueia a conta
            original_account = AccountModel.objects.select_for_update().get(id=instance.original_account.id)
            account_transferred = AccountModel.objects.select_for_update().get(id=instance.account_transferred.id)

            if instance.processed:
                return
            
            # setar try/except
            # primeira transação (da conta que enviou o dinheiro)
            first_transaction = TransactionModel(
                account=original_account,
                value=instance.value,
                type_transaction=TypeTransactionChoices.EXPENSE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )
            
            # segunda transação (da conta que recebeu o dinheiro)
            second_transaction = TransactionModel(
                account=account_transferred,
                value=instance.value,
                type_transaction=TypeTransactionChoices.RECIPE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )

            TransactionService.create_transaction(first_transaction)
            TransactionService.create_transaction(second_transaction)

            instance.processed = True
            instance.save(update_fields=['processed'])

            django_transaction.on_commit(
                lambda: TransactionService.send_email_when_transfer_created(
                    instance
                )
            )

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransferModel.objects.get(transfer_root=instance)
        
    @staticmethod
    @django_transaction.atomic
    def update_transaction(old_instance, new_instance):
        account = (
            AccountModel.objects
            .select_for_update()
            .get(id=new_instance.account_id)
        )

        old_value = old_instance.value
        new_value = new_instance.value

        old_type = old_instance.type_transaction
        new_type = new_instance.type_transaction

        # desfaz impacto antigo
        if old_type == 'RECEITA':
            account.balance -= old_value
        else:
            account.balance += old_value

        # aplica impacto novo
        if new_type == 'RECEITA':
            account.balance += new_value
        else:
            account.balance -= new_value

        account.save()

    @staticmethod
    @django_transaction.atomic
    def delete_transaction(instance: TransactionModel | RecurringTransactionModel):
        if instance.type_transaction == 'RECEITA':
            instance.account.balance -= instance.value
        else:
            instance.account.balance += instance.value

        instance.account.save()
        instance.delete()
    
    @staticmethod
    @django_transaction.atomic
    def delete_transfer(instance: TransferModel):
        transctions = TransactionModel.objects.filter(transfer_root=instance)
        transctions.delete()

        instance.account_transferred.balance -= instance.value
        instance.original_account.balance += instance.value
        instance.original_account.save(update_fields=['balance'])
        instance.account_transferred.save(update_fields=['balance'])

        instance.delete()
        
    # TODO: criar function para quando excluir uma recurring transaction

    # ENVIO DE EMAILS

    @staticmethod
    def send_email_when_recurring_transaction_created(instance: RecurringTransactionModel):
        from apps.base.tasks import send_email_task

        # dados do usuário
        first_name = instance.account.user.first_name
        email = instance.account.user.email

        # dados da transação
        description = instance.description
        value = instance.value
        frequency = instance.frequency
        init_date = timezone.localtime(instance.init_date)
        next_run_date = timezone.localtime(instance.next_run_date)

        message = message_recurring_transaction_created(
            first_name,
            description,
            value,
            frequency,
            init_date.strftime('%d/%m/%Y, %H:%M:%S'),
            next_run_date.strftime('%d/%m/%Y, %H:%M:%S')
        )

        send_email_task.delay(
            subject=message['email_subject'],
            message=message['email_body'],
            recipient_list=[email]
        )

    @staticmethod
    def send_email_when_transfer_created(instance: TransferModel):
        from apps.base.tasks import send_email_task

        # dados do usuário
        first_name = instance.original_account.user.first_name
        email = instance.original_account.user.email

        # dados da transferência
        value = instance.value
        original_account = instance.original_account
        account_transferred = instance.account_transferred
        datetime = timezone.localtime(instance.created_at)

        message = message_transfer_completed(
            first_name,
            value,
            original_account,
            account_transferred,
            datetime.strftime('%d/%m/%Y, %H:%M:%S')
        )

        send_email_task.delay(
            subject=message['email_subject'],
            message=message['email_body'],
            recipient_list=[email]
        )
