from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.category.models import CategoryModel


class DetailCategorySerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer(read_only=True)
    
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
            'account',
        ]
