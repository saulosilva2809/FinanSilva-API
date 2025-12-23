from rest_framework import serializers

from apps.transaction.models import TransactionModel


class CreateUpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('id', 'account', 'type_transaction', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        return value
