from django.db import models

from apps.base.models import BaseModel


class CategoryModel(BaseModel):
    account = models.ForeignKey('account.AccountModel', on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-created_at"]
