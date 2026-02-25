from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView

from .schema_views import SpectacularV1APIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api_v1_urls')),

    # documentação
    path('api/v1/schema/', SpectacularV1APIView.as_view(urlconf='apps.api_v1_urls'), name='schema-v1'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema-v1'),),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
