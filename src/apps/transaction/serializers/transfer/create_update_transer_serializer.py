from rest_framework import serializers

from apps.transaction.models import TransferModel


class CreateUpdateTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = (
            'id', 'original_account', 'account_transferred', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor da transferência deve ser maior que zero.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        original_account = attrs.get('original_account')
        account_transferred = attrs.get('account_transferred')
        value = attrs.get('value')

        if original_account == account_transferred:
            raise serializers.ValidationError({
                'account_transferred': 'A conta de destino não pode ser a mesma que a conta de origem.'
            })

        
        if original_account and original_account.user != user:
            raise serializers.ValidationError({
                'original_account': 'Você não tem permissão para realizar transferências a partir desta conta.'
            })

        if account_transferred and account_transferred.user != user:
            raise serializers.ValidationError({
                'account_transferred': 'Você só pode transferir para contas que pertencem a você.'
            })

        if original_account and value and value > original_account.balance:
            raise serializers.ValidationError({
                'value': 'Você não possui saldo suficiente nesta conta para realizar esta transferência.'
            })

        return attrs
