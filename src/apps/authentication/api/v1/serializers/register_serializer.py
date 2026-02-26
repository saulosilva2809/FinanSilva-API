from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.authentication.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=UserModel.objects.all(),
                message='Este e-mail já está cadastrado.'
            )
        ],
        error_messages={
            'required': 'O e-mail é obrigatório.',
            'invalid': 'Insira um formato de e-mail válido.'
        }
    )

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True, 'error_messages': {'required': 'O nome é obrigatório.'}},
            'last_name': {'required': True, 'error_messages': {'required': 'O sobrenome é obrigatório.'}},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'As senhas não coincidem.'})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['username'] = validated_data['email']
        user = UserModel.objects.create_user(**validated_data)
        return user