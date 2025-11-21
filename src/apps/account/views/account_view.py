from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.account.models import AccountModel
from apps.account.serializers import (
    CreateAccountSerializer,
    UpdateAccountSerializer,
    ViewAccountSerializer
)
from apps.base.pagination import PaginationAPI


class AccountListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    def get_queryset(self):
        queryset = AccountModel.objects.filter(user=self.request.user)
        params = self.request.query_params

        # filters
        name = params.get('name')
        bank = params.get('bank')
        type_account = params.get('type_account')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if bank:
            queryset = queryset.filter(bank=bank)

        if type_account:
            queryset = queryset.filter(type_account=type_account)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAccountSerializer
        return ViewAccountSerializer

class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateAccountSerializer
        return ViewAccountSerializer
