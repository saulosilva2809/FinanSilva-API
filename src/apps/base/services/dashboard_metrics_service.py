from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.account.models.choices import TypeAccountChoices
from apps.transaction.models import TransactionModel, RecurringTransactionModel
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

    def _has_filters(self):
        return any([
            self.category,
            self.subcategory,
            self.start_date,
            self.end_date,
        ])


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
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .aggregate(total=Sum("value"))["total"] or 0
        )

        total_expense = (
            self.transactions.filter(
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
                type_transaction=TypeTransactionChoices.RECIPE
            )
            .exclude(category__isnull=True)
            .values("category__name", 'category__id')
            .annotate(total=Sum("value"))
        )

        expenses_qs = (
            self.transactions.filter(
                type_transaction=TypeTransactionChoices.EXPENSE
            )
            .exclude(category__isnull=True)
            .values("category__name", 'category__id')
            .annotate(total=Sum("value"))
        )

        return {
            "income_by_category": [{
                'category': {
                    'name': item["category__name"],
                    'id': item["category__id"],
                }, 
                'value': item["total"] or 0}
                for item in recipes_qs
            ],
            "expenses_by_category": [{
                'category': {
                    'name': item["category__name"],
                    'id': item["category__id"],
                },
                'value': item["total"] or 0}
                for item in expenses_qs
            ]}

    def get_monthly_summary(self):
        recipes_qs = (
            self.transactions.filter(
                type_transaction=TypeTransactionChoices.RECIPE,
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("value"))
            .order_by("month")
        )

        expenses_qs = (
            self.transactions.filter(
                type_transaction=TypeTransactionChoices.EXPENSE,
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
    
    def recent_transactions(self):
        transactions = (
            self.transactions
            .select_related('account', 'category')
            .order_by('-created_at')[:5]
        )

        return [
            {
                "id": ts.id,
                "value": float(ts.value),
                "type_transaction": ts.type_transaction,
                "created_at": ts.created_at,
                "account": {
                    "id": ts.account.id,
                    "name": ts.account.name,
                },
                "category": {
                    "id": ts.category.id,
                    "name": ts.category.name,
                } if ts.category else None,
            }
            for ts in transactions
        ]

    
    def upcoming_transactions(self):
        rec_transactions = RecurringTransactionModel.objects.filter(
            active=True
        ).select_related(
            'account', 'category'
        ).order_by('next_run_date')[:5]

        return [
            {
                'id': ts.id,
                'value': float(ts.value),
                'type_transaction': ts.type_transaction,
                'frequency': ts.frequency,
                'next_run_date': ts.next_run_date,
                'init_date': ts.init_date,
                'account': {
                    'id': ts.account.id,
                    'name': ts.account.name,
                },
                'category': {
                    'id': ts.category.id,
                    'name': ts.category.name,
                } if ts.category else None,
            }
            for ts in rec_transactions
        ]
    
    def set_response(self):
        response = {
            'total_global_values': self.total_global_values(),
            'values_by_category': self.values_by_category(),
            'monthly_summary': self.get_monthly_summary(),
            'recents_transactions': self.recent_transactions(),
            'upcoming_transactions': self.upcoming_transactions(),
        }

        if self._has_filters():
            response['total_filtered_values'] = self.total_filtered_values()

        return response
