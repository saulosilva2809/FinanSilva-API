from rest_framework import serializers

from apps.account.models import AccountModel


class UpdateAccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = AccountModel
        fields = ('name', 'bank', 'type_account', 'description', 'initial_balance', 'balance')

    def validate_initial_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("O saldo inicial não pode ser negativo.")
        return value

    def update(self, instance, validated_data):
        new_initial = validated_data.get('initial_balance', instance.initial_balance)
        diff = new_initial - instance.initial_balance
        instance.balance += diff
        return super().update(instance, validated_data)
