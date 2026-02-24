from django.db.models import QuerySet
from uuid import uuid4

from apps.account.models import AccountModel
from apps.authentication.models import UserModel


class AccountSelector:
    @staticmethod
    def get_accounts_by_user(user: UserModel) -> QuerySet[AccountModel]:
        return AccountModel.objects.filter(user=user)

    @staticmethod
    def get_account_by_id(id: uuid4) -> AccountModel:
        return AccountModel.objects.select_for_update().get(id=id)
