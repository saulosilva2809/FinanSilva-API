from rest_framework import generics, permissions

from apps.category.models import CategoryModel
from apps.category.serializers import CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryModel.objects.filter(account__in=self.request.user.accounts.all())


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = CategorySerializer

    def get_queryset(self):
        return CategoryModel.objects.filter(account__in=self.request.user.accounts.all())
