from django.contrib import admin
from django.db import transaction

from .models import RecurringTransactionModel, TransactionModel, TransferModel
from apps.transaction.services import TransactionService, TransferService


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'account', 'value', 'type_transaction', 'recurring_root', 'transfer_root')

    # para várias exclusões
    def delete_queryset(self, request, queryset):
        with transaction.atomic():
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
        with transaction.atomic():
            for obj in queryset:
                TransferService.delete_transfer(obj)

    def delete_model(self, request, obj):
        TransferService.delete_transfer(obj)
