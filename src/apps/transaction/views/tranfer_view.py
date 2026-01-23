from django.db.models import Q
from rest_framework import generics, permissions

from apps.base.pagination import PaginationAPI
from apps.transaction.models import TransferModel
from apps.transaction.serializers import (
    CreateUpdateTransferSerializer,
    DetailTransferSerializer,
    ListTransferSerializer,
)
from apps.transaction.services import TransferService


class TransferListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    def get_queryset(self):
        user_accounts = self.request.user.accounts.all()
        return TransferModel.objects.filter(
            Q(original_account__in=user_accounts) |
            Q(account_transferred__in=user_accounts)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateTransferSerializer
        return ListTransferSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        TransferService.create_transaction_from_transfer(instance)


class TransferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        user_accounts = self.request.user.accounts.all()
        return TransferModel.objects.filter(
            Q(original_account__in=user_accounts) |
            Q(account_transferred__in=user_accounts)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransferSerializer
        return DetailTransferSerializer
    
    def perform_destroy(self, instance):
        TransferService.delete_transfer(instance)
