from django.db.models import QuerySet, Q

from apps.authentication.models import UserModel
from apps.transaction.models import TransferModel


class TransferSelector:
    @staticmethod
    def get_transfers_by_user(user: UserModel) -> QuerySet[TransferModel]:
        return (
            TransferModel.objects
            .filter(
                Q(original_account__user=user) |
                Q(account_transferred__user=user)
            )
            .select_related(
                'original_account',
                'account_transferred',
                'category',
                'subcategory'
            )
            .order_by('-created_at')
        )
