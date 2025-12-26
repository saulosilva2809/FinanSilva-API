from rest_framework import generics, permissions

from apps.base.pagination import PaginationAPI
from apps.transaction.models import TransferModel
from apps.transaction.serializers import (
    CreateUpdateTransferSerializer,
    DetailTransferSerializer,
    ListTransferSerializer,
)
from apps.transaction.services import TransactionService


class TransferListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    def get_queryset(self):
        return TransferModel.objects.filter(original_account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateTransferSerializer
        return ListTransferSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        TransactionService.create_transaction_from_transfer(self.request, instance)


class TransferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransferModel.objects.filter(original_account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransferSerializer
        return DetailTransferSerializer
