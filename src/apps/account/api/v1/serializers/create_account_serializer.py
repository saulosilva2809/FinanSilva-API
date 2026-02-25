from rest_framework import serializers

from apps.account.models import AccountModel


class CreateAccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S', read_only=True)

    class Meta:
        model = AccountModel
        fields = ('id', 'name', 'bank', 'type_account', 'description', 'initial_balance', 'balance', 'created_at')

    def validate_initial_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("O saldo inicial não pode ser negativo.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
