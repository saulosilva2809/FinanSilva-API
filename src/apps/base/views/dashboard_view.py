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
        queryset = AccountModel.objects.filter(user=self.request.user)
        queryset = self.filter_queryset(queryset)

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
