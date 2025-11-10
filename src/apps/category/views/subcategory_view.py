from rest_framework import generics, permissions

from apps.category.models import SubCategoryModel
from apps.category.serializers import SubCategorySerializer


class SubCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategoryModel.objects.filter(
            category__account__in=self.request.user.accounts.all()
        )


class SubCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return SubCategoryModel.objects.filter(category__account__in=self.request.user.accounts.all())
