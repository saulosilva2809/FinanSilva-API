import django_filters

from apps.transaction.models import TransactionModel


class TransactionFilter(django_filters.FilterSet):
    account_id = django_filters.UUIDFilter(field_name='account__id')
    account_name = django_filters.CharFilter(field_name='account__name', lookup_expr='icontains')

    higher_value = django_filters.NumberFilter(field_name='value', lookup_expr='gte')
    lower_value = django_filters.NumberFilter(field_name='value', lookup_expr='lte')

    category_id = django_filters.CharFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    subcategory_id = django_filters.UUIDFilter(field_name='subcategory__id')
    subcategory_name = django_filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')

    type_transaction = django_filters.CharFilter()
    recurring_root = django_filters.UUIDFilter(field_name='recurring_root__id')

    class Meta:
        model = TransactionModel
        fields = []
