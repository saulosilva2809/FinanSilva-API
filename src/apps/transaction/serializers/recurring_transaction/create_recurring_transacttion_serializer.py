from rest_framework import serializers

from apps.transaction.models import RecurringTransactionModel


class CreateRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = ('id', 'account', 'value', 'type_transaction', 'description', 'frequency', 'active', 'category', 'subcategory', 'init_date')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        return value
