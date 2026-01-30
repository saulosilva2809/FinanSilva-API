from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from apps.base.pagination import PaginationAPI
from apps.category.filters import SubCategoryFilter
from apps.category.models import SubCategoryModel
from apps.category.serializers import (
    CreateUpdateSubCategorySerializer,
    DetailSubCategorySerializer,
    ListSubCategorySerializer,
)


class SubCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubCategoryFilter

    def get_queryset(self):
        return SubCategoryModel.objects.filter(
            category__account__user=self.request.user
        ).select_related('category')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateSubCategorySerializer
        return ListSubCategorySerializer


class SubCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return SubCategoryModel.objects.filter(
            category__account__user=self.request.user
        ).select_related('category')
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateSubCategorySerializer
        return DetailSubCategorySerializer
