from django.db import models

from . import RecurringTransactionModel
from .choices import TypeTransactionChoices
from apps.account.models import AccountModel
from apps.base.models import BaseModel
from apps.category.models import CategoryModel
from apps.category.models import SubCategoryModel


class TransactionModel(BaseModel):
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='transactions')
    type_transaction = models.CharField(choices=TypeTransactionChoices.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2)
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

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            if self.type_transaction == TypeTransactionChoices.RECIPE:
                self.account.balance += self.value
            else:
                self.account.balance -= self.value

            self.account.save()
        
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        ordering = ["-created_at"]
