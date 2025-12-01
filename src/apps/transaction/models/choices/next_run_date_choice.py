from django.db import models


class NextRunDateChoices(models.TextChoices):
    DAILY = "DAILY", "Diária"
    WEEKLY = "WEEKLY", "Semanal"
    BIWEEKLY = "BIWEEKLY", "Quinzenal"
    MONTHLY = "MONTHLY", "Mensal"
    BIMONTHLY = "BIMONTHLY", "Bimestral"
    QUARTERLY = "QUARTERLY", "Trimestral"
    SEMIANNUAL = "SEMIANNUAL", "Semestral"
    ANNUAL = "ANNUAL", "Anual"
