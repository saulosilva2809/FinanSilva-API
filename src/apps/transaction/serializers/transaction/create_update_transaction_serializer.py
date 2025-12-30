from rest_framework import serializers

from apps.account.models import AccountModel
from apps.transaction.models.choices import TypeTransactionChoices
from apps.transaction.models import TransactionModel


class CreateUpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('id', 'account', 'type_transaction', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        
        account = AccountModel.objects.get(id=self.initial_data.get('account'))
        if self.initial_data.get('type_transaction') == TypeTransactionChoices.EXPENSE:
            if value > account.balance:
                raise serializers.ValidationError('Você não possui saldo sulficiente.')

        return value
