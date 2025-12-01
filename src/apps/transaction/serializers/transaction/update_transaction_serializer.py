from rest_framework import serializers

from apps.transaction.models import TransactionModel


class UpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('account', 'type_transaction', 'value', 'description', 'category', 'subcategory')

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("O valor da transação não pode ser negativo.")
        return value
    
    def update(self, instance, validated_data):
        new_value = validated_data.get('value', instance.value)

        if instance.type_transaction == 'RECEITA':
            instance.account.balance -= instance.value
            instance.account.balance += new_value
            instance.account.save()
        
        else:
            instance.account.balance += instance.value
            instance.account.balance -= new_value
            instance.account.save()

        return super().update(instance, validated_data)
