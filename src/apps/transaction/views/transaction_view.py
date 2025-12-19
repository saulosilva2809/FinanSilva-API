from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from apps.transaction.filters import TransactionFilter
from apps.transaction.models import TransactionModel
from apps.transaction.serializers import (
    CreateTransactionSerializer,
    DetailTransactionSerializer,
    ListTransactionSerializer,
    UpdateTransactionSerializer
)
from apps.transaction.services import TransactionService


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return TransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTransactionSerializer
        return ListTransactionSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        TransactionService.create_transaction(instance)


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateTransactionSerializer
        return DetailTransactionSerializer
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        new_instance = serializer.save()

        TransactionService.update_transaction(
            old_instance=old_instance,
            new_instance=new_instance
        )

