from rest_framework import generics, permissions

from apps.account.models import AccountModel
from apps.account.serializers import (
    CreateAccountSerializer,
    UpdateAccountSerializer,
    ViewAccountSerializer
)


class AccountListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAccountSerializer
        return ViewAccountSerializer


class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateAccountSerializer
        return ViewAccountSerializer
