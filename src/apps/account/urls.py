from django.urls import path, include


urlpatterns = [
    path('', include('apps.account.api.v1.urls'))
]
