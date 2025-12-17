from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.category.models import SubCategoryModel


class SubCategorySerializer(serializers.ModelSerializer):
    category = BaseMiniSerializer(read_only=True)
    
    class Meta:
        model = SubCategoryModel
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
            'category',
        ]
