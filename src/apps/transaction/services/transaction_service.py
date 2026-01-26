import logging

from django.db import IntegrityError, transaction as django_transaction

from apps.account.models import AccountModel
from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices


logger = logging.getLogger(__name__)

class TransactionService:
    @staticmethod
    @django_transaction.atomic
    def update_balance_account(instance: TransactionModel):
        try:
            account = (
                AccountModel.objects
                .select_for_update()
                .get(id=instance.account_id)
            )

            if instance.processed:
                return

            if instance.type_transaction == TypeTransactionChoices.RECIPE:
                account.balance += instance.value
            else:
                account.balance -= instance.value

            account.save()

            instance.processed = True
            instance.save(update_fields=["processed"])

            return instance

        except IntegrityError:
            # idempotency_key repetida → retorna a transação original
            return TransactionModel.objects.get(
                idempotency_key=instance.idempotency_key
            )
        
    @staticmethod
    @django_transaction.atomic
    def update_transaction(old_instance, new_instance):
        account = (
            AccountModel.objects
            .select_for_update()
            .get(id=new_instance.account_id)
        )

        old_value = old_instance.value
        new_value = new_instance.value

        old_type = old_instance.type_transaction
        new_type = new_instance.type_transaction

        # desfaz impacto antigo
        if old_type == TypeTransactionChoices.RECIPE:
            account.balance -= old_value
        else:
            account.balance += old_value

        # aplica impacto novo
        if new_type == TypeTransactionChoices.RECIPE:
            account.balance += new_value
        else:
            account.balance -= new_value

        account.save()

    @staticmethod
    @django_transaction.atomic
    def delete_transaction(instance: TransactionModel):
        account = AccountModel.objects.select_for_update().get(id=instance.account.id)

        if instance.type_transaction == 'RECEITA':
            account.balance -= instance.value
        else:
            account.balance += instance.value

        instance.account.save()
        instance.delete()
