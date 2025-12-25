from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.category.models import SubCategoryModel


class DetailSubCategorySerializer(serializers.ModelSerializer):
    category = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    
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
