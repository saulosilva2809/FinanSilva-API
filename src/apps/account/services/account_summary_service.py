from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now

from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices


class AccountSummary:
    def __init__(self, queryset):
        self.queryset = queryset
        self.today = now().date()
        self.one_year_ago = self.today.replace(day=1) - timedelta(days=365)

    def total_values(self):
        total_accounts = self.queryset.count()
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

        return {
            "total_accounts": total_accounts,
            "total_balance": total_balance,
            "total_recipe": total_recipe,
            "total_expense": total_expense,
        }

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
        # ** para fazer merge de dicts
        return {
            **self.total_values(),
            **self.values_by_category(),
            **self.get_monthly_summary(),
        }
