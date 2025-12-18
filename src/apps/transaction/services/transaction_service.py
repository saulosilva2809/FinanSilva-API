import uuid

from django.db import IntegrityError, transaction

from apps.account.models import AccountModel
from apps.transaction.models import RecurringTransactionModel, TransactionModel


class TransactionService:

    @staticmethod
    @transaction.atomic
    def create_transaction(instance: TransactionModel):
        try:
            account = (
                AccountModel.objects
                .select_for_update()
                .get(id=instance.account_id)
            )

            if instance.processed:
                return

            if instance.type_transaction == 'RECEITA':
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
    @transaction.atomic
    def create_transaction_from_recurring_transaction(instance: RecurringTransactionModel):
        try:
            # bloqueia a conta
            account = AccountModel.objects.select_for_update().get(id=instance.account_id)

            # não processar duas vezes
            if instance.processed:
                return

            # cria a transação real
            tx = TransactionModel.objects.create(
                account=account,
                value=instance.value,
                type_transaction=instance.type_transaction,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                idempotency_key=uuid.uuid4(),
                processed=True
            )

            # aplica saldo
            if tx.type_transaction == 'RECEITA':
                account.balance += tx.value
            else:
                account.balance -= tx.value
            account.save()

            # marca a recorrente como processada na primeira execução
            instance.processed = True
            instance.executed_first_time = True
            instance.save(update_fields=["processed", "executed_first_time"])

            return tx

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransactionModel.objects.get(idempotency_key=tx.idempotency_key)

    @staticmethod
    @transaction.atomic
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
        if old_type == 'RECEITA':
            account.balance -= old_value
        else:
            account.balance += old_value

        # aplica impacto novo
        if new_type == 'RECEITA':
            account.balance += new_value
        else:
            account.balance -= new_value

        account.save()
