from rest_framework.serializers import ModelSerializer

from apps.authentication.models import UserModel


class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # aplica na instância

        instance.save(update_fields=validated_data.keys())  # salva só o que mudou
        return instance
