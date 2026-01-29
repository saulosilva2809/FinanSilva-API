from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from apps.base.pagination import PaginationAPI
from apps.transaction.filters import TransactionFilter
from apps.transaction.models import TransactionModel
from apps.transaction.serializers import (
    CreateUpdateTransactionSerializer,
    DetailTransactionSerializer,
    ListTransactionSerializer,
)
from apps.transaction.services import TransactionService


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
    filter_backends = [DjangoFilterBackend]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return TransactionModel.objects.filter(
            account__user=self.request.user
        ).select_related(
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'transfer_root',
            'transfer_root__original_account',
            'transfer_root__account_transferred'
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateTransactionSerializer
        return ListTransactionSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        TransactionService.update_balance_account(instance)


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransactionSerializer
        return DetailTransactionSerializer
    
    def perform_destroy(self, instance):
        TransactionService.delete_transaction(instance)
    
    def perform_update(self, serializer):
        old_instance = self.get_object()
        new_instance = serializer.save()

        TransactionService.update_transaction(
            old_instance=old_instance,
            new_instance=new_instance
        )
