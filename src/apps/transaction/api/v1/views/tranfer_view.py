from rest_framework import generics, permissions

from apps.base.pagination import PaginationAPI
from apps.transaction.api.v1.serializers import (
    CreateUpdateTransferSerializer,
    DetailTransferSerializer,
    ListTransferSerializer,
)
from apps.transaction.selectors import TransferSelector
from apps.transaction.services import TransferService
from apps.transaction.permissions import IsTransferOnwer


class TransferListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    def get_queryset(self):
        return TransferSelector.get_transfers_by_user(self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateTransferSerializer
        return ListTransferSerializer
    
    def perform_create(self, serializer):
        TransferService.create_transfer(serializer.validated_data)


class TransferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsTransferOnwer]
    lookup_field = 'pk'

    def get_queryset(self):
        return TransferSelector.get_transfers_by_user(self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransferSerializer
        return DetailTransferSerializer
    
    def perform_destroy(self, instance):
        TransferService.delete_transfer(instance)
