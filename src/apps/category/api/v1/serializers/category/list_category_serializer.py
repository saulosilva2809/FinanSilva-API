from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.category.models import CategoryModel


class ListCategorySerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'account',
        ]
