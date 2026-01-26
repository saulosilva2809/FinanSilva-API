import json

from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.transaction.email_messages import message_recurring_transaction_created
from apps.transaction.models import RecurringTransactionModel


@receiver(post_save, sender=RecurringTransactionModel)
def create_task_celery_to_recurring_transaction(sender, instance: RecurringTransactionModel, created, **kwargs):
    from apps.base.tasks import send_email_task

    if created and instance.active:
        run_date = instance.init_date
        run_date = timezone.localtime(run_date)

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

        transaction.on_commit(
            lambda: send_email_task.delay(
                subject=message['email_subject'],
                message=message['email_body'],
                recipient_list=[email]
            )
        )
        
@receiver(pre_delete, sender=RecurringTransactionModel)
def delete_celery_task_post_delete_transaction(sender, instance, **kwargs):
    with transaction.atomic():
        periodic_task = PeriodicTask.objects.filter(
            name=f'transaction_{instance.id}'
        )

        if periodic_task:
            periodic_task.delete()
