from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from apps.base.pagination import PaginationAPI
from apps.category.filters import CategoryFilter
from apps.category.models import CategoryModel
from apps.category.serializers import (
    DetailCategorySerializer,
    CreateUpdateCategorySerializer,
    ListCategorySerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        return CategoryModel.objects.filter(
            account__user=self.request.user
        ).select_related('account')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateCategorySerializer
        return ListCategorySerializer
    

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return CategoryModel.objects.filter(
            account__user=self.request.user
        ).select_related('account')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateCategorySerializer
        return DetailCategorySerializer
