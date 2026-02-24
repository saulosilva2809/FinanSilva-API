from rest_framework import serializers

from apps.transaction.models import TransactionModel


class CreateUpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('id', 'account', 'type_transaction', 'value', 'description', 'category', 'subcategory')

    def validate(self, data):
        value = data.get('value')

        if value < 0:
            raise serializers.ValidationError({"value": "O valor não pode ser negativo."})

        return data
