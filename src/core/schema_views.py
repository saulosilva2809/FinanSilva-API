from drf_spectacular.settings import spectacular_settings
from drf_spectacular.views import SpectacularAPIView


class SpectacularV1APIView(SpectacularAPIView):
    def get(self, request, *args, **kwargs):
        spectacular_settings.SERVERS = [{'url': '/api/v1'}]
        return super().get(request, *args, **kwargs)


class SpectacularV2APIView(SpectacularAPIView):
    def get(self, request, *args, **kwargs):
        spectacular_settings.SERVERS = [{'url': '/api/v2'}]
        return super().get(request, *args, **kwargs)
