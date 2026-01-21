import json
import logging

from celery import shared_task
from django.db import transaction
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.transaction.models import RecurringTransactionModel
from apps.transaction.services import TransactionService


logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=30, retry_kwargs={'max_retries': 5})
def process_recurring_transaction(self, recurring_id):
    try:
        with transaction.atomic():
            rec = RecurringTransactionModel.objects.select_for_update().get(id=recurring_id)

            logger.info('Criando Transaction para Recurring Transaction')
            TransactionService.create_transaction_from_recurring_transaction(rec)

            # calcula próxima data
            next_date = rec.set_next_run_date()
            rec.executed_first_time = True
            rec.next_run_date = next_date
            rec.save()

            logger.info('Criando novo ClockedSchedule')
            clocked = ClockedSchedule.objects.create(
                clocked_time=next_date
            )

            logger.info('Apagando a PeriodicTask e ClockedSchedule anterior')
            old_task = PeriodicTask.objects.filter(
                name=f"transaction_{rec.id}",
            ).first()
            if old_task:
                old_next_time = old_task.clocked
                old_task.delete()

                if old_next_time:
                    old_next_time.delete()

            logger.info('Criando nova PeriodicTask')
            PeriodicTask.objects.create(
                name=f"transaction_{rec.id}",
                task="apps.base.tasks.process_recurring_transaction_task.process_recurring_transaction",
                clocked=clocked,
                one_off=True,
                args=json.dumps([str(rec.id)]),
            )

            # TODO: definir o envio de email aqui

    except Exception as e:
        logger.exception(f'Erro inesperado: {e}')
        raise
