import uuid

from django.db import models

from apps.base.models import BaseModel


class TransferModel(BaseModel):
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    processed = models.BooleanField(default=False)
    original_account = models.ForeignKey('account.AccountModel', on_delete=models.CASCADE, related_name='transfers_sent')
    account_transferred = models.ForeignKey('account.AccountModel', on_delete=models.CASCADE, related_name='transfers_received')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'category.CategoryModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transfers'
    )
    subcategory = models.ForeignKey(
        'category.SubCategoryModel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transfers'
    )

    class Meta:
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=['original_account', '-created_at']),
            models.Index(fields=['account_transferred', '-created_at'])
        ]
