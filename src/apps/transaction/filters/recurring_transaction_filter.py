import django_filters

from apps.transaction.models import RecurringTransactionModel


class RecurringTransactionFilter(django_filters.FilterSet):
    account_id = django_filters.UUIDFilter(field_name='account__id')
    account_name = django_filters.CharFilter(field_name='account__name', lookup_expr='icontains')

    higher_value = django_filters.NumberFilter(field_name='value', lookup_expr='gte')
    lower_value = django_filters.NumberFilter(field_name='value', lookup_expr='lte')

    category_id = django_filters.UUIDFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    subcategory_id = django_filters.UUIDFilter(field_name='subcategory__id')
    subcategory_name = django_filters.CharFilter(field_name='subcategory__name', lookup_expr='icontains')

    type_transaction = django_filters.CharFilter(field_name='type_transaction')
    frequency = django_filters.CharFilter(field_name='frequency')
    active = django_filters.BooleanFilter(field_name='active')

    next_run_date = django_filters.DateFilter(field_name='next_run_date', lookup_expr='date')
    date_start_run = django_filters.DateTimeFilter(field_name='next_run_date', lookup_expr='gte')
    date_end_run = django_filters.DateTimeFilter(field_name='next_run_date', lookup_expr='lte')

    class Meta:
        model = RecurringTransactionModel
        fields = []
