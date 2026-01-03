from django.db import transaction
from functools import partial
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.base.tasks import approve_recurring_transaction
from apps.base.pagination import PaginationAPI
from apps.transaction.models import RecurringTransactionModel
from apps.transaction.serializers import (
    CreateUpdateRecurringTransactionSerializer,
    DetailRecurringTransactionSerializer,
    ListRecurringTransactionSerializer,
    RecurringTransactionSummarySerializer,
    SimulateApprovalInputSerializer,
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


class SimulateApprovalRecurringTransaction(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecurringTransactionSummarySerializer
    
    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(
            account__in=self.request.user.accounts.all()
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        input_serializer = SimulateApprovalInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        ref_date = input_serializer.validated_data.get('reference_date')

        output_serializer = self.get_serializer(
            instance,
            context={'reference_date': ref_date}
        )

        return Response(output_serializer.data)

class ApproveRecurringTransactionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return RecurringTransactionModel.objects.filter(
            account__in=self.request.user.accounts.all()
        )

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.active:
            return Response(
                {"error": "Esta transação recorrente está inativa."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # O on_commit garante que a Task só dispare se o banco confirmar a transação
            transaction.on_commit(
                partial(
                    approve_recurring_transaction.delay,
                    recurring_id=instance.id
                )
            )

        return Response(
            {
                "id": instance.id,
                "status": "processing",
                "message": (
                    "Antecipação aceita para processamento. "
                    "Você receberá uma notificação quando o lançamento for concluído."
                )
            },
            status=status.HTTP_202_ACCEPTED
        )
