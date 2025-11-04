from django.db import models

from apps.account.models import AccountModel
from apps.base.models import BaseModel


class CategoryModel(BaseModel):
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-created_at"]
