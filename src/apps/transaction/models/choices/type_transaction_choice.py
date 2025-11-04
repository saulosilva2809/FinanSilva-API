from django.db import models


class TypeTransactionChoices(models.TextChoices):
    # TODO: implementar modo de transações entre contas
    RECIPE = "RECEITA", "Receita"
    EXPENSE = "DESPESA", "Despesa"
    DEFAULT = "UNDEFINED", "Undefined"
