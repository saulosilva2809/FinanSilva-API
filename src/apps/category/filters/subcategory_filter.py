import django_filters

from apps.category.models import SubCategoryModel


class SubCategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = SubCategoryModel
        fields = []
