from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.transaction.models import TransactionModel


@receiver(post_delete, sender=TransactionModel)
def update_balance_post_delete_transaction(sender, instance, **kwargs):
    # TODO: implementar type TRANSFERENCIA quando criado
    if instance.type_transaction == 'RECEITA':
        instance.account.balance -= instance.value
    elif instance.type_transaction == 'DESPESA':
        instance.account.balance += instance.value
    
    instance.account.save()
