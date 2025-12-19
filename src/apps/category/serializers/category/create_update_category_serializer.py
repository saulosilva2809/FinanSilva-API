from rest_framework import serializers

from apps.category.models import CategoryModel


class CreateUpdateCategorySerializer(serializers.ModelSerializer):
    # TODO: refatorar para mostrar nome da conta e id
    class Meta:
        model = CategoryModel
        fields = [
            'id',
            'name',
            'description',
            'account',
        ]
