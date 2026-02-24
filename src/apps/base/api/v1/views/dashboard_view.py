from rest_framework import generics, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.base.filters import DashboardFilter
from apps.base.services import DashboardMetrics
from apps.account.models import AccountModel


class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DashboardFilter

    def get_queryset(self, request):
        return AccountModel.objects.filter(user=self.request.user)

    def get(self, request):
        queryset_base = self.get_queryset(self.request)
        filtered_accounts = self.filter_queryset(queryset_base)
        params = self.request.query_params

        category = params.get('category')
        subcategory = params.get('subcategory')
        start_date = params.get('start_date')
        end_date = params.get('end_date')

        service = DashboardMetrics(
            request=self.request,
            queryset=filtered_accounts,
            category=category,
            subcategory=subcategory,
            start_date=start_date,
            end_date=end_date,
        )

        response_data = service.get_cached_dashboard()

        return Response(response_data)
