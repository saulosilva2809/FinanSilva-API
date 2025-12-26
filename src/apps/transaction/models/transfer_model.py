import uuid

from django.db import models

from apps.account.models import AccountModel
from apps.base.models import BaseModel
from apps.category.models import CategoryModel, SubCategoryModel


class TransferModel(BaseModel):
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    processed = models.BooleanField(default=False)
    original_account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='transfers_sent')
    account_transferred = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='transfers_received')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        CategoryModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transfers'
    )
    subcategory = models.ForeignKey(
        SubCategoryModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transfers'
    )

    class Meta:
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"
        ordering = ["-created_at"]
