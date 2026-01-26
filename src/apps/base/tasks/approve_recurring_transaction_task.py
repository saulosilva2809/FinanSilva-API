import json
import logging

from celery import shared_task
from django.db import transaction
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.base.email_messages import message_approve_recurring_transaction
from apps.base.tasks import send_email_task # se der circular import volta essa import para dentro da def
from apps.transaction.models import RecurringTransactionModel


logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=30, retry_kwargs={'max_retries': 5})
def approve_recurring_transaction(self, recurring_id):
    from apps.transaction.services import RecurringTransactionService
    try:
        with transaction.atomic():
            # pegando a rec no db
            rec = RecurringTransactionModel.objects.select_for_update().get(id=recurring_id)

            # criando a transaction com base na rec
            RecurringTransactionService.create_transaction_from_recurring_transaction(rec)

            # marca como executado pela primeira vez e marca o horário da ultima vez que executou
            rec.executed_first_time = True
            rec.executed_last_time = rec.next_run_date
            rec.save(update_fields=["executed_first_time", "executed_last_time"])

            # setando novo horário
            old_next_time = rec.next_run_date
            next_date = rec.set_next_run_date()
            rec.next_run_date = next_date
            rec.save(update_fields=["next_run_date"])

            # deletando agendamento de horário antigo
            ClockedSchedule.objects.filter(
                clocked_time=old_next_time
            ).delete()

            # criando o novo agendamento de hprário
            clocked = ClockedSchedule.objects.create(
                clocked_time=next_date
            )

            # apagando agendamento de task
            PeriodicTask.objects.filter(
                name=f"transaction_{rec.id}"
            ).delete()

            # criando o novo agendamento de task
            PeriodicTask.objects.create(
                name=f"transaction_{rec.id}",
                task="apps.base.tasks.process_recurring_transaction_task.process_recurring_transaction",
                clocked=clocked,
                one_off=True,
                args=json.dumps([str(rec.id)]),
            )

        # preparando o email
        old_time_fmt = timezone.localtime(old_next_time).strftime('%d/%m/%Y %H:%M')
        new_time_fmt = timezone.localtime(next_date).strftime('%d/%m/%Y %H:%M')
        updated_at = timezone.localtime(rec.updated_at).strftime('%d/%m/%Y %H:%M')

        messages = message_approve_recurring_transaction(rec, old_time_fmt, updated_at, new_time_fmt)

        # enviando o e-mail usando a task 
        transaction.on_commit(
            lambda: send_email_task.delay(
                subject=messages['email_subject'],
                message=messages['email_body'],
                recipient_list=[rec.account.user.email]
            )
        )

    except Exception as e:
        logger.exception(f"Erro ao aprovar transação {recurring_id}")
        raise
