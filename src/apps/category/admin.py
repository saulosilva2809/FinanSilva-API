from django.contrib import admin

from .models import CategoryModel, SubCategoryModel


admin.site.register(CategoryModel)
admin.site.register(SubCategoryModel)
