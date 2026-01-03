import json

from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.transaction.models import RecurringTransactionModel


@receiver(post_save, sender=RecurringTransactionModel)
def create_task_celery_to_recurring_transaction(sender, instance: RecurringTransactionModel, created, **kwargs):
    if created and instance.active:
        run_date = instance.init_date

        instance.next_run_date = instance.set_next_run_date()
        instance.save(update_fields=['next_run_date'])

        clocked = ClockedSchedule.objects.create(
            clocked_time=run_date
        )

        PeriodicTask.objects.create(
            name=f"transaction_{instance.id}",
            task="apps.base.tasks.process_recurring_transaction_task.process_recurring_transaction",
            clocked=clocked,
            one_off=True,
            args=json.dumps([str(instance.id)]),
        )

@receiver(pre_delete, sender=RecurringTransactionModel)
def delete_celery_task_post_delete_transaction(sender, instance, **kwargs):
    with transaction.atomic():
        periodic_task = PeriodicTask.objects.filter(
            name=f'transaction_{instance.id}'
        )

        if periodic_task:
            periodic_task.delete()
