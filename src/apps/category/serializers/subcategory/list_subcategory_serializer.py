from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.category.models import CategoryModel


class ListSubCategorySerializer(serializers.ModelSerializer):
    category = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'category',
        ]
