from django.db.models import QuerySet
from uuid import uuid4

from apps.account.models import AccountModel
from apps.authentication.models import UserModel


class AccountSelector:
    @staticmethod
    def get_accounts_by_user(view_instance, user: UserModel) -> QuerySet[AccountModel]:
        if getattr(view_instance, 'swagger_fake_view', False):
            return AccountModel.objects.none()

        return AccountModel.objects.filter(user=user)

    @staticmethod
    def get_account_by_id(id: uuid4) -> AccountModel:
        return AccountModel.objects.select_for_update().get(id=id)
