from django.db import models

from .choices import TypeTransactionChoices
from apps.account.models import AccountModel
from apps.base.models import BaseModel
from apps.category.models import CategoryModel


class TransactionModel(BaseModel):
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    type_transaction = models.CharField(choices=TypeTransactionChoices.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        CategoryModel,
        default=TypeTransactionChoices.DEFAULT,
        on_delete=models.SET_DEFAULT,
    )
    
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-created_at"]
