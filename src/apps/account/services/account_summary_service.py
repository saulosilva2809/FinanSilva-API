from django.db.models import Count
from django.utils.timezone import now


class AccountSummary:
    def __init__(self, queryset):
        self.queryset = queryset
        self.today = now().date()

    def total_values(self):
        total_accounts = self.queryset.count()

        return {"total_accounts": total_accounts,}
    
    def number_accounts_by_type(self): # métrica que retorna quantidade de contas por tipo
        qs = (
            self.queryset
            .values('type_account')
            .annotate(
                total=Count('id')
            )
            .order_by('type_account')
        )

        return {
            'number_accounts_by_type': qs
        }

    def set_response(self):
        # ** para fazer merge de dicts
        return {
            **self.total_values(),
            **self.number_accounts_by_type(),
            # **self.values_by_category(),
            # **self.get_monthly_summary(),
        }
