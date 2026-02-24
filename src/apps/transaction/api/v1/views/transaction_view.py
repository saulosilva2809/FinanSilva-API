from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, response, status

from apps.base.pagination import PaginationAPI
from apps.transaction.api.v1.serializers import (
    CreateUpdateRecurringTransactionSerializer,
    CreateUpdateTransactionSerializer,
    DetailTransactionSerializer,
    ListTransactionSerializer,
)
from apps.transaction.filters import TransactionFilter
from apps.transaction.models import TransactionModel
from apps.transaction.services import TransactionService
from apps.transaction.permissions import IsTransactionOnwer


class TransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
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
            'transfer_root'
        ).prefetch_related(
            'transfer_root__original_account',
            'transfer_root__account_transferred'
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateTransactionSerializer
        return ListTransactionSerializer
    
    def perform_create(self, serializer):
        TransactionService.create_transaction(serializer.validated_data)


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTransactionOnwer]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransactionModel.objects.filter(
            account__user=self.request.user
        ).select_related(
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'transfer_root'
        ).prefetch_related(
            'transfer_root__original_account',
            'transfer_root__account_transferred'
        )

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


class ConvertTransactionInRecurringTransactionView(generics.GenericAPIView):
    permissions = [permissions.IsAuthenticated, IsTransactionOnwer]
    serializer_class = CreateUpdateRecurringTransactionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return TransactionModel.objects.filter(
            account__user=self.request.user
        ).select_related(
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'transfer_root'
        ).prefetch_related(
            'transfer_root__original_account',
            'transfer_root__account_transferred'
        )
    
    def post(self, request, *args, **kwargs):
        transaction = self.get_object()

        data = request.data.copy()
        print(data, flush=True)

        data.update({
            'account': transaction.account.id,
            'value': transaction.value,
            'type_transaction': transaction.type_transaction,
            'description': transaction.description,
            'category': transaction.category.id if transaction.category else None,
            'subcategory': transaction.subcategory.id if transaction.subcategory else None,
        })

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        TransactionService.create_recurring_transaction_from_transaction(serializer.validated_data)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
