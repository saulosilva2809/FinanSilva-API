from rest_framework import serializers

from apps.account.models import AccountModel
from apps.transaction.models import TransferModel


class CreateUpdateTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = ('id', 'original_account', 'account_transferred', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        print(f'VALUE: {self.initial_data.get("value")}')
        if value < 0:
            raise serializers.ValidationError(
                "O valor da transação não pode ser negativo."
            )

        original_account_id = self.initial_data.get("original_account")
        account_transferred_id = self.initial_data.get("account_transferred")

        if original_account_id == account_transferred_id:
            raise serializers.ValidationError(
                "A conta de origem não pode ser a mesma que a conta de destino."
            )
        
        original_account_model = AccountModel.objects.get(id=original_account_id)

        if value > original_account_model.balance:
            raise serializers.ValidationError(
                'Você não possui saldo sulficiente.'
            )
        
        return value
