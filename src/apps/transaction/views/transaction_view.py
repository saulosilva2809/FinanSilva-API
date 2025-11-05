from rest_framework import generics, permissions

from apps.transaction.models import TransactionModel
from apps.transaction.serializers import (
    CreateTransactionSerializer,
    ViewTransactionSerializer
)


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionModel.objects.filter(account_in=self.request.user.accounts)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTransactionSerializer
        return ViewTransactionSerializer
