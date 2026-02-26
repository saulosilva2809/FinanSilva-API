from rest_framework import serializers

from apps.authentication.models import UserModel


class ViewProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S')

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'created_at', 'updated_at')
