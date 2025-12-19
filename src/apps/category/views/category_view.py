from rest_framework import generics, permissions

from apps.category.models import CategoryModel
from apps.category.serializers import (
    CategorySerializer,
    CreateUpdateCategorySerializer,
    ListCategorySerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # TODO: implementar filters com django-filter
    def get_queryset(self):
        return CategoryModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateCategorySerializer
        return ListCategorySerializer
    

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateCategorySerializer
        return CategorySerializer
