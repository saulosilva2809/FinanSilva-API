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
        q1 = TransferModel.objects.filter(original_account__user=self.request.user)
        q2 = TransferModel.objects.filter(account_transferred__user=self.request.user)
        transfers = q1.union(q2).order_by('-created_at')

        return transfers

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
        q1 = TransferModel.objects.filter(original_account__user=self.request.user)
        q2 = TransferModel.objects.filter(account_transferred__user=self.request.user)
        transfers = q1.union(q2).order_by('-created_at')

        return transfers

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransferSerializer
        return DetailTransferSerializer
    
    def perform_destroy(self, instance):
        TransferService.delete_transfer(instance)
