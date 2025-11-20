from datetime import timedelta, date
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from apps.account.models.choices import TypeAccountChoices
from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices

# TODO: continuar trabalhando no Dashboard
class DashboardMetrics():
    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset
        self.one_year_ago = date.today() - timedelta(days=365)

    def total_values(self):
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

        total_saved = self.queryset.filter(
            type_account__in=[
                TypeAccountChoices.INVESTMENT, 
                TypeAccountChoices.SAVINGS
            ]
        ).aggregate(total=Sum("balance"))["total"] or 0

        return {
            'total_balance': total_balance,
            'total_recipe': total_recipe,
            'total_expense': total_expense,
            'total_saved': total_saved,
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
            "recipes_by_category": [
                {'category': item["category__name"], 'value': item["total"] or 0}
                for item in recipes_qs
            ],
            "expenses_by_category": [
                {'category': item["category__name"], 'value': item["total"] or 0}
                for item in expenses_qs
            ],
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

        recipes_by_month = {
            item["month"].strftime("%Y-%m"): item["total"] or 0
            for item in recipes_qs
        }
        expenses_by_month = {
            item["month"].strftime("%Y-%m"): item["total"] or 0
            for item in expenses_qs
        }
        months = set(recipes_by_month) | set(expenses_by_month)
        
        summary = {}
        for month in months:
            recipes = recipes_by_month.get(month, 0)
            expenses = expenses_by_month.get(month, 0)

            summary[month] = {
                'recipes': recipes,
                'expenses': expenses,
                'balance': recipes - expenses
            }

        return summary
    
    def recents_transactions(self):
        transactions = TransactionModel.objects.order_by('-created_at')[:5].values(
            'account', 'type_transaction', 'value', 'category', 'created_at'
        )

        return transactions
    
    def set_response(self):
        return {
            'total_values': self.total_values(),
            'values_by_category': self.values_by_category(),
            'monthly_summary': self.get_monthly_summary(),
            'recents_transactions': self.recents_transactions(),
        }
