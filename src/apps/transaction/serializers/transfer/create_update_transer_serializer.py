from rest_framework import serializers

from apps.transaction.models import TransferModel


class CreateUpdateTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = ('id', 'original_account', 'account_transferred', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        return value
