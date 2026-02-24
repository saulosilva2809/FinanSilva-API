from rest_framework import generics, permissions

from apps.base.pagination import PaginationAPI
from apps.transaction.api.v1.serializers import (
    CreateUpdateTransferSerializer,
    DetailTransferSerializer,
    ListTransferSerializer,
)
from apps.transaction.models import TransferModel
from apps.transaction.services import TransferService
from apps.transaction.permissions import IsTransferOnwer


class TransferListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    def get_queryset(self):
        q1 = TransferModel.objects.filter(original_account__user=self.request.user)
        q2 = TransferModel.objects.filter(account_transferred__user=self.request.user)

        transfers = q1.union(q2).order_by('-created_at').prefetch_related(
            'original_account', 
            'account_transferred', 
            'category', 
            'subcategory'
        )

        return transfers

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
        q1 = TransferModel.objects.filter(original_account__user=self.request.user)
        q2 = TransferModel.objects.filter(account_transferred__user=self.request.user)

        transfers = q1.union(q2).order_by('-created_at').prefetch_related(
            'original_account', 
            'account_transferred', 
            'category', 
            'subcategory'
        )

        return transfers

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateTransferSerializer
        return DetailTransferSerializer
    
    def perform_destroy(self, instance):
        TransferService.delete_transfer(instance)
