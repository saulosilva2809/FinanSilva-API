from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.account.models.choices import TypeAccountChoices
from apps.transaction.models import TransactionModel
from apps.transaction.models.choices import TypeTransactionChoices


class DashboardMetrics():
    def __init__(
            self, request, queryset,
            category=None, subcategory=None,
            start_date=None, end_date=None
        ):
        self.request = request
        self.queryset = queryset
        self.one_year_ago = timezone.now() - timedelta(days=365)
        self.category = category
        self.subcategory = subcategory
        self.start_date = start_date
        self.end_date = end_date
        self.transactions = self._filter_transactions()

    def _filter_transactions(self):
        filters = {"account__in": self.queryset}

        if self.start_date:
            filters["created_at__gte"] = self.start_date

        if self.end_date:
            filters["created_at__lte"] = self.end_date

        if self.category:
            filters['category'] = self.category

        if self.subcategory:
            filters['subcategory'] = self.subcategory

        return TransactionModel.objects.filter(**filters)

    def total_filtered_values(self):
        total_recipe = (
            self.transactions.filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .aggregate(total=Sum("value"))["total"] or 0
        )

        total_expense = (
            self.transactions.filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.EXPENSE
            )
            .aggregate(total=Sum("value"))["total"] or 0
        )

        return {
            'total_balance': total_recipe - total_expense,
            'total_recipe': total_recipe,
            'total_expense': total_expense,
        }
    
    def total_global_values(self):
        total_balance = self.queryset.aggregate(total=Sum("balance"))["total"] or 0

        total_saved = self.queryset.filter(
            type_account__in=[
                TypeAccountChoices.INVESTMENT, 
                TypeAccountChoices.SAVINGS
            ]
        ).aggregate(total=Sum("balance"))["total"] or 0

        return {
            'total_balance': total_balance,
            'total_saved': total_saved,
        }

    def values_by_category(self):
        recipes_qs = (
            self.transactions.filter(
                account__in=self.queryset,
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .exclude(category__isnull=True)
            .values("category__name")
            .annotate(total=Sum("value"))
        )

        expenses_qs = (
            self.transactions.filter(
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
            self.transactions.filter(
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
            self.transactions.filter(
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
        transactions = self.transactions.filter(account__in=self.queryset).order_by('-created_at')[:5].values(
            'account', 'type_transaction', 'value', 'category', 'created_at'
        )

        return transactions
    
    def set_response(self):
        return {
            'total_global_values': self.total_global_values(),
            'total_filtered_values': self.total_filtered_values(),
            'values_by_category': self.values_by_category(),
            'monthly_summary': self.get_monthly_summary(),
            'recents_transactions': self.recents_transactions(),
        }
