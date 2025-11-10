from rest_framework import serializers

from apps.category.models import SubCategoryModel


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryModel
        fields = '__all__'
