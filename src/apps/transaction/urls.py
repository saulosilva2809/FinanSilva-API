from django.urls import path
from .views import (
    RecurringTransactionListCreateView,
    RecurringTransactionRetrieveUpdateDestroyView,
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    TransferListCreateView,
    TransferRetrieveUpdateDestroyView
)


urlpatterns = [
    path('recurring-transaction/', RecurringTransactionListCreateView.as_view(), name='recurring_transaction_list_create'),
    path('recurring-transaction/<uuid:pk>', RecurringTransactionRetrieveUpdateDestroyView.as_view(), name='recurring_transaction_retrieve_update_destroy'),
    path('transaction/', TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('transaction/<uuid:pk>', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction_retrieve_update_destroy'),
    path('transfer/', TransferListCreateView.as_view(), name='transfer_list_create'),
    path('transfer/<uuid:pk>', TransferRetrieveUpdateDestroyView.as_view(), name='transfer_retrieve_update_destroy'),
]
