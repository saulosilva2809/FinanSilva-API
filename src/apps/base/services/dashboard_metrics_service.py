from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.account.services import AccountSummary
from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices

# TODO: continuar trabalhando no Dashboard
class DashboardMetrics(AccountSummary):
    def __init__(self, request, queryset):
        super().__init__(queryset)
        self.request = request
        self.queryset = queryset
        self.one_year_ago = self.today.replace(day=1) - timedelta(days=365)

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

    def values_by_category(self):
        recipes_qs = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .exclude(category__isnull=True)
            .values("category__name")
            .annotate(total=Sum("value"))
        )

        expenses_qs = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.EXPENSE
            )
            .exclude(category__isnull=True)
            .values("category__name")
            .annotate(total=Sum("value"))
        )

        return {
            "recipes_by_category": {
                item["category__name"]: item["total"] or 0
                for item in recipes_qs
            },
            "expenses_by_category": {
                item["category__name"]: item["total"] or 0
                for item in expenses_qs
            },
        }

    def get_monthly_summary(self):
        recipes_qs = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.RECIPE,
                created_at__gte=self.one_year_ago,
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("value"))
            .order_by("month")
        )

        expenses_qs = (
            TransactionModel.objects
            .filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.EXPENSE,
                created_at__gte=self.one_year_ago,
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("value"))
            .order_by("month")
        )

        return {
            "recipes_by_month": {
                item["month"].strftime("%Y-%m"): item["total"] or 0
                for item in recipes_qs
            },
            "expenses_by_month": {
                item["month"].strftime("%Y-%m"): item["total"] or 0
                for item in expenses_qs
            },
        }
    
    def set_response(self):
        context = super().set_response()
        context['values_by_category'] = self.values_by_category()
        context['monthly_summary'] = self.get_monthly_summary()

        return context
