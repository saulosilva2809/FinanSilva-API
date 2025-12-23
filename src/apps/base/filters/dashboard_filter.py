import django_filters

from apps.account.filters import AccountFilter


class DashboardFilter(AccountFilter):
    account_name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    account_bank = django_filters.CharFilter(field_name='bank')
    type_account = django_filters.CharFilter(field_name='type_account')

    class Meta(AccountFilter.Meta):
        fields = []
