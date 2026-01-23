import uuid

from django.db import IntegrityError, transaction as django_transaction
from django.utils import timezone
from django_celery_beat.models import PeriodicTask

from apps.account.models import AccountModel
from apps.transaction.email_messages import (
    message_recurring_transaction_created,
)
from apps.transaction.models import RecurringTransactionModel, TransactionModel
from apps.transaction.services import TransactionService


class RecurringTransactionService:
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
    