from django.urls import path

from apps.account.api.v1.views import (
    AccountListCreateView,
    AccountRetrieveUpdateDestroyView
)


urlpatterns = [
    path('account/', AccountListCreateView.as_view(), name='account_list_create'),
    path('account/<uuid:pk>', AccountRetrieveUpdateDestroyView.as_view(), name='account_retrieve_update_destroy'),
]
