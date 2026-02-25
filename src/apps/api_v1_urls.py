from django.urls import include, path


urlpatterns = [
    path('', include('apps.account.api.v1.urls')),
    path('', include('apps.authentication.api.v1.urls')),
    path('', include('apps.base.api.v1.urls')),
    path('', include('apps.category.api.v1.urls')),
    path('', include('apps.transaction.api.v1.urls')),
]