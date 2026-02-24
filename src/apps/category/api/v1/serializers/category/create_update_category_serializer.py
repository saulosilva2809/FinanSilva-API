from rest_framework import serializers

from apps.category.models import CategoryModel


class CreateUpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'description',
            'account',
        ]
