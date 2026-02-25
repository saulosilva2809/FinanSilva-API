from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from apps.account.api.v1.serializers import (
    CreateAccountSerializer,
    UpdateAccountSerializer,
    ViewAccountSerializer
)
from apps.account.filters import AccountFilter
from apps.account.selector import AccountSelector
from apps.account.services import AccountService
from apps.base.pagination import PaginationAPI


class AccountListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI
    filter_backends = [DjangoFilterBackend]
    filterset_class = AccountFilter

    def get_queryset(self):
        return AccountSelector.get_accounts_by_user(self, self.request.user)

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
        return AccountSelector.get_accounts_by_user(self, self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateAccountSerializer
        return ViewAccountSerializer
    
    def perform_destroy(self, instance):
        AccountService().delete_account(instance)
