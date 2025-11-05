from django.db import models

from apps.base.models import BaseModel
from apps.category.models import CategoryModel


class SubCategoryModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Sub Categoria"
        verbose_name_plural = "Sub Categorias"
        ordering = ["-created_at"]
