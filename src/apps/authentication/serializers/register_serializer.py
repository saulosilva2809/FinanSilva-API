from rest_framework.serializers import ModelSerializer

from apps.authentication.models import UserModel


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = UserModel.objects.create_user(**validated_data)
        return user
