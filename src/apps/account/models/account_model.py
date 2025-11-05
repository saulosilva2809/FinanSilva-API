from django.db import models

from .choices import BankChoices, TypeAccountChoices
from apps.authentication.models import UserModel
from apps.base.models import BaseModel


class AccountModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=200)
    bank = models.CharField(
        max_length=30,
        choices=BankChoices.choices,
        default=BankChoices.OTHER,
    )
    type_account = models.CharField(
        max_length=20,
        choices=TypeAccountChoices.choices,
        default=TypeAccountChoices.CHECKING,
    )
    description = models.TextField(null=True, blank=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.balance is None:  # apenas na criação
            self.balance = self.initial_balance
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.get_type_account_display()})"

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        ordering = ["-created_at"]
