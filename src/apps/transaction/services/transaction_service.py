import logging

from django.db import IntegrityError, transaction as django_transaction
from rest_framework.exceptions import ValidationError

from apps.account.models import AccountModel
from apps.transaction.email_messages import message_transaction_converted_to_recurring
from apps.transaction.models import TransactionModel, RecurringTransactionModel
from apps.transaction.models.choices import TypeTransactionChoices


logger = logging.getLogger(__name__)

class TransactionService:
    @staticmethod
    @django_transaction.atomic
    def create_transaction(data):
        account = AccountModel.objects.select_for_update().get(
            id=data['account'].id
        )

        if data['type_transaction'] == TypeTransactionChoices.EXPENSE:
            if data['value'] > account.balance:
                raise ValidationError('Saldo insuficiente.')

        instance = TransactionModel.objects.create(**data)
        TransactionService.update_balance_account(instance, account)

        return instance
    
    @staticmethod
    @django_transaction.atomic
    def create_recurring_transaction_from_transaction(data):
        account = data['account'] 
        account_locked = AccountModel.objects.select_for_update().get(id=account.id)

        # cria a transação real
        transaction = RecurringTransactionModel.objects.create(
            account=account_locked,
            value=data['value'],
            type_transaction=data['type_transaction'],
            description=data['description'],
            frequency=data['frequency'],
            active=data.get('active', True),
            category=data['category'],
            subcategory=data['subcategory'],
            executed_first_time=False
        )
    
        django_transaction.on_commit(
            lambda: TransactionService.send_email_when_recurring_transaction_created_from_transaction(
                transaction
            )
        )

        return transaction

    @staticmethod
    @django_transaction.atomic
    def update_balance_account(instance: TransactionModel, account: AccountModel):
        try:
            if not account:
                account = AccountModel.objects.select_for_update().get(id=instance.account_id)

            if instance.processed:
                return

            if instance.type_transaction == TypeTransactionChoices.RECIPE:
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
        if old_type == TypeTransactionChoices.RECIPE:
            account.balance -= old_value
        else:
            account.balance += old_value

        # aplica impacto novo
        if new_type == TypeTransactionChoices.RECIPE:
            account.balance += new_value
        else:
            account.balance -= new_value

        account.save()

    @staticmethod
    @django_transaction.atomic
    def delete_transaction(instance: TransactionModel):
        account = AccountModel.objects.select_for_update().get(id=instance.account.id)

        if instance.type_transaction == TypeTransactionChoices.RECIPE:
            account.balance -= instance.value
        else:
            account.balance += instance.value

        account.save()
        instance.delete()

    @staticmethod
    def send_email_when_recurring_transaction_created_from_transaction(instance: RecurringTransactionModel):
        from apps.base.tasks import send_email_task

        # dados do usuário
        first_name = instance.account.user.first_name
        email = instance.account.user.email

        # dados da transferência
        description = instance.description
        value = instance.value
        frequency = instance.frequency
        next_run_date = instance.next_run_date

        message = message_transaction_converted_to_recurring(
            first_name,
            description,
            value,
            frequency,
            next_run_date
        )

        send_email_task.delay(
            subject=message['email_subject'],
            message=message['email_body'],
            recipient_list=[email]
        )
