from rest_framework import serializers

from apps.authentication.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        print(password, flush=True)
        print(confirm_password, flush=True)

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'As senhas não coincidem.'})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['username'] = validated_data['email']
        user = UserModel.objects.create_user(**validated_data)
    
        return user
