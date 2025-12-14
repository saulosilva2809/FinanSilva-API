from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.base.services import DashboardMetrics
from apps.account.models import AccountModel


class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, request):
        queryset = AccountModel.objects.filter(user=self.request.user)
        params = self.request.query_params

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
        params = self.request.query_params
        category = params.get('category')
        subcategory = params.get('subcategory')
        start_date = params.get('start_date')
        end_date = params.get('end_date')

        service = DashboardMetrics(
            request=self.request,
            queryset=self.get_queryset(self.request),
            category=category,
            subcategory=subcategory,
            start_date=start_date,
            end_date=end_date,
        )

        return Response(service.set_response())
