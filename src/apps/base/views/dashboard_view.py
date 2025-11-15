from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.base.services import DashboardMetrics


class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = DashboardMetrics(request)

        return Response(service.set_response())
