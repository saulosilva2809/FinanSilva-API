import uuid

from django.db import models

from .choices import TypeTransactionChoices
from apps.base.models import BaseModel


class TransactionModel(BaseModel):
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    processed = models.BooleanField(default=False)
    account = models.ForeignKey('account.AccountModel', on_delete=models.CASCADE, related_name='transactions')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(choices=TypeTransactionChoices.choices)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'category.CategoryModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    subcategory = models.ForeignKey(
        'category.SubCategoryModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    recurring_root = models.ForeignKey(
        'transaction.RecurringTransactionModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='generated_transactions'
    )
    transfer_root = models.ForeignKey(
        'transaction.TransferModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='generated_transactions'
    )

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['type_transaction', '-created_at'])
        ]
