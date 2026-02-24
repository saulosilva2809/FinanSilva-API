from django.db.models import QuerySet
from uuid import uuid4

from apps.authentication.models import UserModel
from apps.transaction.models import TransactionModel


class TransactionSelector:
    @staticmethod
    def get_transactions_by_account_owner(user: UserModel) -> QuerySet[TransactionModel]:
        return TransactionModel.objects.filter(
            account__user=user
        ).select_related(
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'transfer_root'
        ).prefetch_related(
            'transfer_root__original_account',
            'transfer_root__account_transferred'
        )
    
    @staticmethod
    def get_transaction_by_idempotency_key(idempotency_key: uuid4) -> TransactionModel:
        return TransactionModel.objects.get(
                idempotency_key=idempotency_key
            )
