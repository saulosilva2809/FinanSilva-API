from django.urls import path, include


urlpatterns = [
    path('', include('apps.authentication.api.v1.urls'))
]
