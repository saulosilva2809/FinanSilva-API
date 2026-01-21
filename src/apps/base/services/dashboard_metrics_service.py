import hashlib
import logging

from datetime import timedelta
from django.core.cache import cache
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.account.models.choices import TypeAccountChoices
from apps.transaction.models import RecurringTransactionModel, TransactionModel, TransferModel
from apps.transaction.models.choices import TypeTransactionChoices


logger = logging.getLogger(__name__)

class DashboardMetrics():
    def __init__(
            self, request, queryset,
            category=None, subcategory=None,
            start_date=None, end_date=None
        ):
        self.request = request
        self.queryset = queryset
        self.account_ids = list(queryset.values_list('id', flat=True))
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
        filters = {"account_id__in": self.account_ids}
        filters['transfer_root__isnull'] = True

        if self.start_date:
            filters["created_at__gte"] = self.start_date

        if self.end_date:
            filters["created_at__lte"] = self.end_date

        if self.category:
            filters['category'] = self.category

        if self.subcategory:
            filters['subcategory'] = self.subcategory

        return TransactionModel.objects.select_related(
            'account', 'category', 'subcategory'
        ).filter(**filters)

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
        from apps.account.models import AccountModel

        stats = AccountModel.objects.filter(id__in=self.account_ids).aggregate(
            total_balance=Sum("balance"),
            total_saved=Sum("balance", filter=Q(type_account__in=[
                TypeAccountChoices.INVESTMENT, 
                TypeAccountChoices.SAVINGS
            ]))
        )

        return {
            'total_balance': stats['total_balance'] or 0,
            'total_saved': stats['total_saved'] or 0,
        }

    def values_by_category(self):
        categories_qs = (
            self.transactions
            .values("category__id", "category__name")
            .annotate(
                income=Sum("value", filter=Q(type_transaction=TypeTransactionChoices.RECIPE)),
                expense=Sum("value", filter=Q(type_transaction=TypeTransactionChoices.EXPENSE))
            )
        )

        income_list = []
        expense_list = []

        for item in categories_qs:
            if item["income"] and item["income"] > 0:
                income_list.append({
                    'category': {'id': item["category__id"], 'name': item["category__name"]},
                    'value': item["income"]
                })

            if item["expense"] and item["expense"] > 0:
                expense_list.append({
                    'category': {'id': item["category__id"], 'name': item["category__name"]},
                    'value': item["expense"]
                })

        return {
            "income_by_category": income_list,
            "expenses_by_category": expense_list
        }

    def get_monthly_summary(self):
        summary_qs = (
            self.transactions
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(
                total_recipes=Sum("value", filter=Q(type_transaction=TypeTransactionChoices.RECIPE)),
                total_expenses=Sum("value", filter=Q(type_transaction=TypeTransactionChoices.EXPENSE))
            )
            .order_by("month")
        )

        transfers_qs = (
            TransferModel.objects.filter(
                Q(original_account_id__in=self.account_ids) |
                Q(account_transferred_id__in=self.account_ids)
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Sum("value"))
            .order_by("month")
        )

        summary = {}
        
        for item in summary_qs:
            month_str = item["month"].strftime("%Y-%m")
            recipes = item["total_recipes"] or 0
            expenses = item["total_expenses"] or 0
            summary[month_str] = {
                'recipes': recipes,
                'expenses': expenses,
                'transfers': 0,
                'balance': recipes - expenses
            }

        for item in transfers_qs:
            month_str = item["month"].strftime("%Y-%m")
            total_transfer = item["total"] or 0
            if month_str in summary:
                summary[month_str]['transfers'] = total_transfer
            else:
                summary[month_str] = {
                    'recipes': 0, 'expenses': 0, 
                    'transfers': total_transfer, 'balance': 0
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
                "subcategory": {
                    "id": ts.subcategory.id,
                    "name": ts.subcategory.name,
                } if ts.subcategory else None,
            }
            for ts in transactions
        ]

    
    def upcoming_transactions(self):
        rec_transactions = RecurringTransactionModel.objects.filter(
            account_id__in=self.account_ids, active=True
        ).select_related(
            'account', 'category'
        ).order_by('next_run_date')[:5]

        return [
            {
                'id': ts.id,
                'value': float(ts.value),
                'type_transaction': ts.type_transaction,
                'frequency': ts.frequency,
                'next_run_date': timezone.localtime(ts.next_run_date),
                'init_date': timezone.localtime(ts.init_date),
                'account': {
                    'id': ts.account.id,
                    'name': ts.account.name,
                },
                'category': {
                    'id': ts.category.id,
                    'name': ts.category.name,
                } if ts.category else None,
                'subcategory': {
                    'id': ts.subcategory.id,
                    'name': ts.subcategory.name,
                } if ts.subcategory else None,
            }
            for ts in rec_transactions
        ]
    
    def recent_transfers(self):
        transfers = TransferModel.objects.select_related(
            'original_account', 'account_transferred', 'category', 'subcategory'
        ).filter(original_account_id__in=self.account_ids)

        return [
            {
                'id': transfer.id,
                'value': float(transfer.value),
                'original_account': {
                    'id': transfer.original_account.id,
                    'name': transfer.original_account.name,
                },
                'account_transferred': {
                    'id': transfer.account_transferred.id,
                    'name': transfer.account_transferred.name,
                },
                'value': transfer.value,
                'created_at': transfer.created_at,
                'category': {
                    'id': transfer.category.id,
                    'name': transfer.category.name,
                } if transfer.category else None,
                'subcategory': {
                    'id': transfer.subcategory.id,
                    'name': transfer.subcategory.name,
                } if transfer.subcategory else None,
            }
            for transfer in transfers
        ]
    
            
    def set_response(self):
        response = {
            'total_global_values': self.total_global_values(),
            'values_by_category': self.values_by_category(),
            'monthly_summary': self.get_monthly_summary(),
            'recents_transactions': self.recent_transactions(),
            'upcoming_transactions': self.upcoming_transactions(),
            'recent_transfers': self.recent_transfers(),
        }

        if self._has_filters():
            response['total_filtered_values'] = self.total_filtered_values()

        return response

    def get_cached_dashboard(self):
        # pega a Query String bruta da URL (ex: "account_name=oi&category=1")
        query_params = self.request.GET.urlencode()
        # cria uma hash curta para a chave não ficar gigante e dar erro
        query_hash = hashlib.md5(query_params.encode()).hexdigest()

        cache_key = f"user_dashboard_{self.request.user.id}_{query_hash}"
        index_key = f'user_dashboard_index_{self.request.user.id}'
        
        data = cache.get(cache_key)
        
        if not data:
            data = self.set_response()
            cache.set(cache_key, data, 3600)

            keys_list = cache.get(index_key, set())
            keys_list.add(cache_key)
            cache.set(index_key, keys_list, 3600)

            logger.info(f"Pegando dados via BD (Filtros: {query_params})")
        else:
            logger.info("Pegando dados via CACHE")
                
        return data
