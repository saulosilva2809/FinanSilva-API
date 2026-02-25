from rest_framework import serializers

from apps.account.models.choices import BankChoices, TypeAccountChoices


class AccountResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    bank = serializers.ChoiceField(choices=BankChoices.choices)
    type_account = serializers.ChoiceField(choices=TypeAccountChoices.choices)
    description = serializers.CharField()
    initial_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
