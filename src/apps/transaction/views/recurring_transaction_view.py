from rest_framework import generics, permissions

from apps.transaction.models import RecurringTransactionModel
from apps.transaction.serializers import (
    CreateRecurringTransactionSerializer,
    DetailRecurringTransactionSerializer,
    ListRecurringTransactionSerializer,
    UpdatRecurringTransactionSerializer,
)
from apps.transaction.services import TransactionService


class RecurringTransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # TODO: implementar filters com django-filter
    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateRecurringTransactionSerializer
        return ListRecurringTransactionSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()

        TransactionService.create_transaction_from_recurring_transaction(instance)


class RecurringTransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdatRecurringTransactionSerializer
        return DetailRecurringTransactionSerializer
