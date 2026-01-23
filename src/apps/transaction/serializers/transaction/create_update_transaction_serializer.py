from rest_framework import serializers

from apps.account.models import AccountModel
from apps.transaction.models.choices import TypeTransactionChoices
from apps.transaction.models import TransactionModel


class CreateUpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('account', 'type_transaction', 'value', 'description', 'category', 'subcategory')

    def validate(self, data):
        account = data.get('account')
        value = data.get('value')
        type_transaction = data.get('type_transaction')

        if value < 0:
            raise serializers.ValidationError({"value": "O valor não pode ser negativo."})

        if type_transaction == TypeTransactionChoices.EXPENSE:
            if value > account.balance:
                raise serializers.ValidationError({"value": "Você não possui saldo suficiente."})

        return data
