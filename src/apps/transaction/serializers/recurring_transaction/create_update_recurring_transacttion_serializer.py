from rest_framework import serializers

from apps.transaction.models.choices import TypeTransactionChoices
from apps.transaction.models import RecurringTransactionModel


class CreateUpdateRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = ('id', 'account', 'value', 'type_transaction', 'description', 'frequency', 'active', 'category', 'subcategory', 'init_date')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")

        if self.initial_data.get('type_transaction') == TypeTransactionChoices.EXPENSE:
            if value > self.initial_data.get('account').balance:
                raise serializers.ValidationError('Você não possui saldo sulficiente.')

        return value
