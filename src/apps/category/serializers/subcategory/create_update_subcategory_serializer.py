from rest_framework import serializers

from apps.category.models import SubCategoryModel


class CreateUpdateSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryModel
        fields = [
            'id',
            'name',
            'description',
            'category',
        ]
