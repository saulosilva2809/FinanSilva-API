from django.db import models


class TypeAccountChoices(models.TextChoices):
        CHECKING = "CORRENTE", "Conta Corrente"
        SAVINGS = "POUPANÇA", "Conta Poupança"
        INVESTMENT = "INVESTIMENTO", "Conta Investimento"
        CASH = "DINHEIRO", "Dinheiro (carteira)"
        CREDIT = "CARTÃO", "Cartão de Crédito"
