from rest_framework import serializers

from apps.transaction.models.choices import TypeTransactionChoices
from apps.transaction.models import RecurringTransactionModel


class CreateUpdateRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = ('id', 'account', 'value', 'type_transaction', 'description', 'frequency', 'active', 'category', 'subcategory', 'init_date')

    def validate(self, attrs):
        # attrs já contém os dados validados pelo DRF (objetos, se forem ForeignKeys)

        value = attrs.get('value')
        type_transaction = attrs.get('type_transaction')
        account = attrs.get('account')

        if type_transaction == TypeTransactionChoices.EXPENSE:
            if value > account.balance:
                raise serializers.ValidationError({
                    'value': 'Você não possui sado suficiente nesta conta.'
                })
        
        return attrs
