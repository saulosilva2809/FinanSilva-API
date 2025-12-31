from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.base.pagination import PaginationAPI
from apps.transaction.models import RecurringTransactionModel
from apps.transaction.serializers import (
    CreateUpdateRecurringTransactionSerializer,
    DetailRecurringTransactionSerializer,
    ListRecurringTransactionSerializer,
)


class RecurringTransactionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PaginationAPI

    # TODO: implementar filters com django-filter
    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUpdateRecurringTransactionSerializer
        return ListRecurringTransactionSerializer


class RecurringTransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(account__in=self.request.user.accounts.all())

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CreateUpdateRecurringTransactionSerializer
        return DetailRecurringTransactionSerializer


class ApproveRecurringTransactionView(generics.GenericAPIView):
    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(account__in=self.request.user.accounts.all())
    
    def post(self):
        rec_id = self.kwargs['id']

        return Response({'id': rec_id})
        