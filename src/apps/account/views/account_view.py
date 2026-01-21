from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from apps.account.filters import AccountFilter
from apps.account.models import AccountModel
from apps.account.serializers import (
    CreateAccountSerializer,
    UpdateAccountSerializer,
    ViewAccountSerializer
)
from apps.account.services import AccountService
from apps.base.pagination import PaginationAPI


class AccountListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAccountSerializer
        return ViewAccountSerializer
    
    def perform_create(self, serializer):
        account_instance = serializer.save()
        AccountService().create_account(account_instance)


class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateAccountSerializer
        return ViewAccountSerializer
    
    def perform_destroy(self, instance):
        AccountService().delete_account(instance)
