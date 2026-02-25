from django.urls import include, path


urlpatterns = [
    path('accounts/', include('apps.account.api.v1.urls')),
    path('auth/', include('apps.authentication.api.v1.urls')),
    path('', include('apps.base.api.v1.urls')),
    path('categories/', include('apps.category.api.v1.urls')),
    path('transactions/', include('apps.transaction.api.v1.urls')),
]