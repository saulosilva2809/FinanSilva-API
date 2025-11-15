from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.account.urls')),
    path('api/v1/', include('apps.category.urls')),
    path('api/v1/', include('apps.transaction.urls')),
    path('api/v1/', include('apps.base.urls')),
]
