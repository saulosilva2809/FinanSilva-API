from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.account.models import AccountModel
from apps.transaction.models import RecurringTransactionModel, TransactionModel, TransferModel


@receiver([post_save, post_delete], sender=AccountModel)
@receiver([post_save, post_delete], sender=RecurringTransactionModel)
@receiver([post_save, post_delete], sender=TransactionModel)
@receiver([post_save, post_delete], sender=TransferModel)
def clear_dashboard_cache(sender, instance, **kwargs):
    if sender == AccountModel:
        user_id = instance.user.id

    elif sender == TransactionModel or sender == RecurringTransactionModel:
        user_id = instance.account.user.id

    elif sender == TransferModel:
        user_id = instance.original_account.user.id

    index_key = f'user_dashboard_index_{user_id}'
    keys_to_delete = cache.get(index_key, set())

    if keys_to_delete:
        cache.delete_many(list(keys_to_delete))
    
    cache.delete(index_key)
