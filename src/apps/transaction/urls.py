from django.urls import path, include


urlpatterns = [
    path('', include('apps.transaction.api.v1.urls')),
]
