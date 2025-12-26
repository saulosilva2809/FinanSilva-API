from django.db import models


class TypeTransactionChoices(models.TextChoices):
    RECIPE = "RECEITA", "Receita"
    EXPENSE = "DESPESA", "Despesa"
