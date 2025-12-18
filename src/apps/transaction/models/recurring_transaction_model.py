import uuid

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.timezone import now, make_aware, is_naive

from .choices import NextRunDateChoices, TypeTransactionChoices
from apps.account.models import AccountModel
from apps.base.models import BaseModel
from apps.category.models import CategoryModel, SubCategoryModel


def default_datetime():
    return now()


class RecurringTransactionModel(BaseModel):
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    processed = models.BooleanField(default=False)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE, related_name='recurring_transactions')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(choices=TypeTransactionChoices.choices, default='')
    description = models.CharField(max_length=255)
    frequency = models.CharField(choices=NextRunDateChoices, max_length=50)
    next_run_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    category = models.ForeignKey(CategoryModel, null=True, blank=True, on_delete=models.SET_NULL, related_name='recurring_transactions')
    subcategory = models.ForeignKey(SubCategoryModel, null=True, blank=True, on_delete=models.SET_NULL, related_name='recurring_transactions')
    init_date = models.DateTimeField(default=default_datetime)
    executed_first_time = models.BooleanField(default=False)
    execute_first_immediately = models.BooleanField(default=False)

    def set_next_run_date(self):
        frequency_dict = {
            NextRunDateChoices.DAILY: {'time': 'days', 'value': 1},
            NextRunDateChoices.WEEKLY: {'time': 'weeks', 'value': 1},
            NextRunDateChoices.BIWEEKLY: {'time': 'days', 'value': 14},
            NextRunDateChoices.MONTHLY: {'time': 'months', 'value': 1},
            NextRunDateChoices.BIMONTHLY: {'time': 'months', 'value': 2},
            NextRunDateChoices.QUARTERLY: {'time': 'months', 'value': 3},
            NextRunDateChoices.SEMIANNUAL: {'time': 'months', 'value': 6},
            NextRunDateChoices.ANNUAL: {'time': 'years', 'value': 1},
        }

        config = frequency_dict[self.frequency]

        base = now()

        if config['time'] in ('days', 'weeks'):
            delta = timedelta(**{config['time']: config['value']})
        else:
            delta = relativedelta(**{config['time']: config['value']})

        next_date = base + delta

        if is_naive(next_date):
            next_date = make_aware(next_date)

        return next_date

    def save(self, *args, **kwargs):
        if not self.next_run_date:
            self.next_run_date = self.set_next_run_date()

        if is_naive(self.next_run_date):
            self.next_run_date = make_aware(self.next_run_date)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Transação Recorrente"
        verbose_name_plural = "Transações Recorrentes"
        ordering = ["-created_at"]
