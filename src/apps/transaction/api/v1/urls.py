from django.urls import path

from .views import (
    ApproveAdvanceRecurringTransactionView,
    ConvertTransactionInRecurringTransactionView,
    RecurringTransactionListCreateView,
    RecurringTransactionRetrieveUpdateDestroyView,
    SimulateApprovalRecurringTransaction,
    TransactionListCreateView,
    TransactionRetrieveUpdateDestroyView,
    TransferListCreateView,
    TransferRetrieveUpdateDestroyView
)


urlpatterns = [
    path('recurring/', RecurringTransactionListCreateView.as_view(), name='recurring_transaction_list_create'),
    path('recurring/<uuid:pk>', RecurringTransactionRetrieveUpdateDestroyView.as_view(), name='recurring_transaction_retrieve_update_destroy'),
    path('recurring/<uuid:pk>/simulate-approval/', SimulateApprovalRecurringTransaction.as_view(), name='simulate_approval_recurring_transaction'),
    path('recurring/<uuid:pk>/approve-advance/', ApproveAdvanceRecurringTransactionView.as_view(), name='approve_advance_recurring_transaction'),

    path('', TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('<uuid:pk>', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction_retrieve_update_destroy'),
    path('<uuid:pk>/convert-in-recurring/', ConvertTransactionInRecurringTransactionView.as_view(), name='convert_transaction_in_recurring_trasaction'),

    path('transfer/', TransferListCreateView.as_view(), name='transfer_list_create'),
    path('transfer/<uuid:pk>', TransferRetrieveUpdateDestroyView.as_view(), name='transfer_retrieve_update_destroy'),
]
