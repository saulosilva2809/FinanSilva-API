import uuid

from django.db import IntegrityError, transaction as django_transaction
from django.utils import timezone
from django_celery_beat.models import PeriodicTask

from apps.account.models import AccountModel
from apps.transaction.email_messages import message_recurring_transaction_success
from apps.transaction.models import RecurringTransactionModel, TransactionModel


class RecurringTransactionService:
    @staticmethod
    @django_transaction.atomic
    def create_transaction_from_recurring_transaction(instance: RecurringTransactionModel):
        from apps.transaction.services import TransactionService
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

            # marca a recorrente como processada na primeira execução
            instance.executed_first_time = True
            instance.executed_last_time = timezone.now()
            instance.save()

            django_transaction.on_commit(
                lambda: RecurringTransactionService.send_email_when_recurring_transaction_executed(
                    instance
                )
            )

            return transaction

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransactionModel.objects.get(idempotency_key=transaction.idempotency_key)
        
    @staticmethod
    @django_transaction.atomic
    def delete_recurring_transaction(instance: RecurringTransactionModel):
        old_task = PeriodicTask.objects.filter(
            name=f"transaction_{instance.id}",
        ).first()
        if old_task:
            old_next_time = old_task.clocked
            old_task.delete()

            if old_next_time:
                old_next_time.delete()

        instance.delete()

    @staticmethod
    def send_email_when_recurring_transaction_executed(instance: RecurringTransactionModel):
        from apps.base.tasks import send_email_task

        # dados do usuário
        first_name = instance.account.user.first_name
        email = instance.account.user.email

        # dados da transação
        description = instance.description
        value = instance.value
        account_name = instance.account.name

        message = message_recurring_transaction_success(
            first_name,
            description,
            value,
            account_name
        )

        send_email_task.apply_async(
        kwargs={
            'subject': message['email_subject'],
            'message': message['email_body'],
            'recipient_list': [email]
        },
        countdown=10 
    )
    