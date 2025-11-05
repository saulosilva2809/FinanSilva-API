from django.urls import path
from .views import TransactionListCreateView


urlpatterns = [
    path('transaction/', TransactionListCreateView.as_view(), name='transaction_list_create'),
]
