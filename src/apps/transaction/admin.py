from django.contrib import admin

from .models import RecurringTransactionModel, TransactionModel, TransferModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'value', 'type_transaction', 'recurring_root')

@admin.register(RecurringTransactionModel)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'value', 'type_transaction', 'init_date', 'next_run_date', 'active')

@admin.register(TransferModel)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('original_account', 'account_transferred', 'value', 'category', 'subcategory')
