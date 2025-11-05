from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveUpdateDestroyView


urlpatterns = [
    path('transaction/', TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('transaction/<uuid:pk>', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction_retrieve_update_destroy'),
]
