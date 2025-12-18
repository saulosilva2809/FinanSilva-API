import uuid

from django.db import models

from . import RecurringTransactionModel
from .choices import TypeTransactionChoices
from apps.account.models import AccountModel
from apps.base.models import BaseModel
from apps.category.models import CategoryModel, SubCategoryModel


class TransactionModel(BaseModel):
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    processed = models.BooleanField(default=False)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='transactions')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(choices=TypeTransactionChoices.choices)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        CategoryModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    subcategory = models.ForeignKey(
        SubCategoryModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='transactions'
    )
    recurring_root = models.ForeignKey(
        RecurringTransactionModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='generated_transactions'
    )

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-created_at"]
