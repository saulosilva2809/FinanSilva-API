import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import make_aware
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.transaction.models import RecurringTransactionModel


@receiver(post_save, sender=RecurringTransactionModel)
def update_or_create_task_celery_to_recurring_transaction(sender, instance, created, **kwargs):
    if created and instance.active:
        if instance.executed_first_time == True:
            run_date = instance.next_run_date
        else:
            run_date = instance.init_date

        if run_date and run_date.tzinfo is None:
            run_date = make_aware(run_date)

        try:
            clocked, _ = ClockedSchedule.objects.get_or_create(
                clocked_time=run_date
            )

            PeriodicTask.objects.update_or_create(
                name=f"transaction_{instance.id}",
                defaults={
                    "task": "apps.base.tasks.process_recurring_transaction_task.process_recurring_transaction",
                    "clocked": clocked,
                    "one_off": True,
                    "enabled": True,
                    "args": json.dumps([str(instance.id)]), 
                }
            )
        
        except Exception as e:
            raise e
