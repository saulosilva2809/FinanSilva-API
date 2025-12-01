from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.transaction.models import TransactionModel


@receiver(post_delete, sender=TransactionModel)
def update_balance_post_delete_transaction(sender, instance, **kwargs):
    if instance.type_transaction == 'RECEITA':
        instance.account.balance -= instance.value
    else:
        instance.account.balance += instance.value
    
    instance.account.save()

