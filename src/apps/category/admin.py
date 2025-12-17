from django.contrib import admin

from .models import CategoryModel, SubCategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'name')

@admin.register(SubCategoryModel)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
