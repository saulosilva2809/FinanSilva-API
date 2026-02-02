from rest_framework import serializers

from apps.transaction.models import RecurringTransactionModel


class ConvertTransactionInRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = [
            'frequency',
            'init_date',
        ]
