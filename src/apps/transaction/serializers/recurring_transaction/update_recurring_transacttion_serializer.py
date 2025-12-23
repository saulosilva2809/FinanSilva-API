from rest_framework import serializers

from apps.transaction.models import RecurringTransactionModel


class UpdatRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = ('account', 'value', 'description', 'frequency', 'active', 'category', 'subcategory')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        return value
