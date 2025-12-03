from celery import shared_task

from apps.transaction.models import RecurringTransactionModel, TransactionModel


@shared_task(bind=True)
def process_recurring_transaction(self, recurring_id):
    try:
        rec = RecurringTransactionModel.objects.get(id=recurring_id)
        
        TransactionModel.objects.create(
            account=rec.account,
            type_transaction=rec.type_transaction,
            value=rec.value,
            description=rec.description,
            category=rec.category,
            subcategory=rec.subcategory,
            recurring_root=rec,
        )

        if not rec.executed_first_time:
            rec.executed_first_time = True

        rec.next_run_date = rec.set_next_run_date()
        rec.save()
    
    except Exception as e:
        raise e
