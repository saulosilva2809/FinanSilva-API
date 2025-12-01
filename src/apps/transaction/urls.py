from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    RecurringTransactionListCreateView,
    RecurringTransactionRetrieveUpdateDestroyView
)


urlpatterns = [
    path('transaction/', TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('transaction/<uuid:pk>', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction_retrieve_update_destroy'),
    path('recurring-transaction/', RecurringTransactionListCreateView.as_view(), name='recurring_transaction_list_create'),
    path('recurring-transaction/<uuid:pk>', RecurringTransactionRetrieveUpdateDestroyView.as_view(), name='recurring_transaction_retrieve_update_destroy'),
]
