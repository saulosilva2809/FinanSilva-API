from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.base.services import DashboardMetrics
from apps.account.models import AccountModel


class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = AccountModel.objects.filter(user=self.request.user)
        params = self.request.query_params

        # filters
        name = params.get('account_name')
        bank = params.get('account_bank')
        type_account = params.get('type_account')

        if name:
            queryset = queryset.filter(name__icontains=name)

        if bank:
            queryset = queryset.filter(bank=bank)

        if type_account:
            queryset = queryset.filter(type_account=type_account)

        return queryset

    def get(self, request):
        service = DashboardMetrics(
            request=request,
            queryset=self.get_queryset(request)
        )

        return Response(service.set_response())
