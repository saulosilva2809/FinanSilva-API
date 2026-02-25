from rest_framework import serializers

from apps.account.models.choices import BankChoices, TypeAccountChoices


class CreateAccountRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    bank = serializers.ChoiceField(choices=BankChoices.choices)
    type_account = serializers.ChoiceField(choices=TypeAccountChoices.choices)
    description = serializers.CharField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)


class CreateAccountResponseSerializer(CreateAccountRequestSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S')
