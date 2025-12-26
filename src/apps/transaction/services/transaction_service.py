import uuid

from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied

from apps.account.models import AccountModel
from apps.transaction.models import RecurringTransactionModel, TransactionModel, TransferModel
from apps.transaction.models.choices import TypeTransactionChoices


class TransactionService:

    @staticmethod
    @transaction.atomic
    def update_balance_accounts(instance: TransactionModel):
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
            transaction = TransactionModel.objects.create(
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
            if transaction.type_transaction == 'RECEITA':
                account.balance += transaction.value
            else:
                account.balance -= transaction.value
            account.save()

            # marca a recorrente como processada na primeira execução
            instance.processed = True
            instance.executed_first_time = True
            instance.save(update_fields=["processed", "executed_first_time"])

            return transaction

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransactionModel.objects.get(idempotency_key=transaction.idempotency_key)

    @staticmethod
    @transaction.atomic
    def create_transaction_from_transfer(request, instance: TransferModel):
        try:
            # bloqueia a conta
            original_account = AccountModel.objects.select_for_update().get(id=instance.original_account.id)
            account_transferred = AccountModel.objects.select_for_update().get(id=instance.account_transferred.id)

            if account_transferred.user != request.user:
                raise PermissionDenied("Você não tem permissão para transferir a essa conta.")

            if instance.processed:
                return
            
            # setar try/except
            # primeira transação (da conta que enviou o dinheiro)
            first_transaction = TransactionModel.objects.create(
                account=original_account,
                value=instance.value,
                type_transaction=TypeTransactionChoices.EXPENSE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )
            
            # segunda transação (da conta que recebeu o dinheiro)
            second_transaction = TransactionModel.objects.create(
                account=account_transferred,
                value=instance.value,
                type_transaction=TypeTransactionChoices.RECIPE,
                description=instance.description,
                category=instance.category,
                subcategory=instance.subcategory,
                transfer_root=instance,
            )

            TransactionService.update_balance_accounts(first_transaction)
            TransactionService.update_balance_accounts(second_transaction)

            instance.processed = True
            instance.save(update_fields=['processed'])

        except IntegrityError:
            # idempotency_key repetida → retorna a transação já criada
            return TransferModel.objects.get(idempotency_key=instance.idempotency_key)

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
