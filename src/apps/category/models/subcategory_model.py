from django.db import models

from apps.base.models import BaseModel


class SubCategoryModel(BaseModel):
    category = models.ForeignKey('category.CategoryModel', on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sub Categoria"
        verbose_name_plural = "Sub Categorias"
        ordering = ["-created_at"]
