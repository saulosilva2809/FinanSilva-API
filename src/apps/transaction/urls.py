from django.urls import path, include


urlpatterns = [
    path('v1/', include('apps.transaction.api.v1.urls')),
]
