from django.db.models import Sum

from apps.account.models import AccountModel
from apps.account.services import AccountSummary
from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices

# TODO: continuar trabalhando no Dashboard
class DashboardMetrics(AccountSummary):
    def __init__(self, request):
        self.request = request
        self.queryset = AccountModel.objects.filter(user=request.user)

    def total_values(self):
        context = super().total_values()

        total_balance = self.queryset.aggregate(total=Sum("balance"))["total"] or 0

        total_recipe = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .aggregate(total=Sum("value"))["total"] or 0
        )

        total_expense = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.EXPENSE
            )
            .aggregate(total=Sum("value"))["total"] or 0
        )

        context['total_balance'] = total_balance
        context['total_recipe'] = total_recipe
        context['total_expense'] = total_expense

        return context
