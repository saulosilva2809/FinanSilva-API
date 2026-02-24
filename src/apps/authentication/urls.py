from django.urls import path, include


urlpatterns = [
    path('v1/auth/', include('apps.authentication.api.v1.urls'))
]
