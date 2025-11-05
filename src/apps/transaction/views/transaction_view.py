from rest_framework import generics, permissions

from apps.transaction.models import TransactionModel
from apps.transaction.serializers import (
    CreateTransactionSerializer,
    UpdateTransactionSerializer,
    ViewTransactionSerializer
)


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTransactionSerializer
        return ViewTransactionSerializer


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateTransactionSerializer
        return ViewTransactionSerializer
