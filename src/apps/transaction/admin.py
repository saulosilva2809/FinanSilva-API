from django.contrib import admin

from .models import RecurringTransactionModel, TransactionModel, TransferModel


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'account', 'value', 'type_transaction', 'recurring_root')

@admin.register(RecurringTransactionModel)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'account', 'value', 'type_transaction', 'init_date', 'next_run_date', 'active', 'executed_first_time', 'executed_last_time')

@admin.register(TransferModel)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'original_account', 'account_transferred', 'value', 'category', 'subcategory')
