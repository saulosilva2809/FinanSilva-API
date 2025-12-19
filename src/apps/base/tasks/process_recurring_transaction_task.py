import json
import logging

from celery import shared_task
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.transaction.models import RecurringTransactionModel, TransactionModel


logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_recurring_transaction(self, recurring_id):
    try:
        rec = RecurringTransactionModel.objects.get(id=recurring_id)

        logger.info('Criando Transaction com base em Recurring Transaction')

        TransactionModel.objects.create(
            account=rec.account,
            type_transaction=rec.type_transaction,
            value=rec.value,
            description=rec.description,
            category=rec.category,
            subcategory=rec.subcategory,
            recurring_root=rec,
        )

        # marca primeira execução
        if not rec.executed_first_time:
            rec.executed_first_time = True

        # calcula próxima data
        next_date = rec.set_next_run_date()
        rec.next_run_date = next_date
        rec.save()

        logger.info('Criando novo ClockedSchedule')
        clocked = ClockedSchedule.objects.create(
            clocked_time=next_date
        )

        logger.info('Apagando a PeriodicTask anterior')
        old_task = PeriodicTask.objects.get(
            name=f"transaction_{rec.id}",
        )
        if old_task:
            old_task.delete()

        logger.info('Criando nova PeriodicTask')
        PeriodicTask.objects.create(
            name=f"transaction_{rec.id}",
            task="apps.base.tasks.process_recurring_transaction_task.process_recurring_transaction",
            clocked=clocked,
            one_off=True,
            args=json.dumps([str(rec.id)]),
        )

    except Exception as e:
        logger.exception(f'Erro inesperado: {e}')
        raise
