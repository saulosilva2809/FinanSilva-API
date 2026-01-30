from django.db import IntegrityError, transaction as django_transaction
from django.utils import timezone

from apps.account.models import AccountModel
from apps.transaction.email_messages import (
    message_transfer_completed,
)
from apps.transaction.models import TransactionModel, TransferModel
from apps.transaction.models.choices import TypeTransactionChoices


class TransferService:
    @staticmethod
    @django_transaction.atomic
    def create_transaction_from_transfer(instance: TransferModel):
        from apps.transaction.services import TransactionService

        try:
            # bloqueia a conta
            original_account = AccountModel.objects.select_for_update().get(id=instance.original_account.id)
            account_transferred = AccountModel.objects.select_for_update().get(id=instance.account_transferred.id)

            if instance.processed:
                return
            
            # setar try/except
            # primeira transação (da conta que enviou o dinheiro)
            first_transaction = TransactionModel.objects.create(
                account=original_account,
                value=instance.value,
                type_transaction=TypeTransactionChoices.EXPENSE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )
            
            # segunda transação (da conta que recebeu o dinheiro)
            second_transaction = TransactionModel.objects.create(
                account=account_transferred,
                value=instance.value,
                type_transaction=TypeTransactionChoices.RECIPE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )

            TransactionService.update_balance_account(first_transaction)
            TransactionService.update_balance_account(second_transaction)

            instance.processed = True
            instance.save(update_fields=['processed'])

            django_transaction.on_commit(
                lambda: TransferService.send_email_when_transfer_created(
                    instance
                )
            )

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransferModel.objects.get(transfer_root=instance)
        
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
