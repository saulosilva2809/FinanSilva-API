from rest_framework.serializers import ModelSerializer

from apps.authentication.models import UserModel


class ViewProfileSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'created_at', 'updated_at')
