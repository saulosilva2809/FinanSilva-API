from django.contrib import admin

from .models import RecurringTransactionModel, TransactionModel, TransferModel
from apps.transaction.services import TransactionService


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'account', 'value', 'type_transaction', 'recurring_root', 'transfer_root')

    # para várias exclusões
    # #TODO: corrija erra aqui, mesmo excluindo todas ele erra no calculo, testar excluindo várias
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            TransactionService.delete_transaction(obj)

    # para uma única
    def delete_model(self, request, obj):
        TransactionService.delete_transaction(obj)


@admin.register(RecurringTransactionModel)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'account', 'value', 'type_transaction', 'init_date', 'next_run_date', 'active', 'executed_first_time', 'executed_last_time')


@admin.register(TransferModel)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'original_account', 'account_transferred', 'value', 'category', 'subcategory')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            TransactionService.delete_transfer(obj)

    def delete_model(self, request, obj):
        TransactionService.delete_transfer(obj)
