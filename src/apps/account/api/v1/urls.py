from django.urls import path

from apps.account.api.v1.views import (
    AccountListCreateView,
    AccountRetrieveUpdateDestroyView
)

from .docs import schemas


urlpatterns = [
    path('', AccountListCreateView.as_view(), name='account_list_create'),
    path('<uuid:pk>', AccountRetrieveUpdateDestroyView.as_view(), name='account_retrieve_update_destroy'),
]
