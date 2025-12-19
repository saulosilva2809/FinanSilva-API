from rest_framework import generics, permissions

from apps.category.models import SubCategoryModel
from apps.category.serializers import (
    ListSubCategorySerializer,
    SubCategorySerializer
)


class SubCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # TODO: implementar filters com django-filter
    def get_queryset(self):
        return SubCategoryModel.objects.filter(
            category__account__in=self.request.user.accounts.all()
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubCategorySerializer
        return ListSubCategorySerializer


class SubCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategoryModel.objects.filter(category__account__in=self.request.user.accounts.all())
