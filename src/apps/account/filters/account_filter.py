import django_filters

from apps.account.models import AccountModel


class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    bank = django_filters.CharFilter(field_name='bank')
    type_account = django_filters.CharFilter(field_name='type_account')

    class Meta:
        model = AccountModel
        fields = []
