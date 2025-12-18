from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import RecurringTransactionModel


class DetailRecurringTransactionSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer()
    category = BaseMiniSerializer()
    subcategory = BaseMiniSerializer()

    class Meta:
        model = RecurringTransactionModel
        fields = [
            'id',
            'value',
            'type_transaction',
            'description',
            'frequency',
            'next_run_date',
            'active',
            'init_date',
            'executed_first_time',
            'execute_first_immediately',
            'account',
            'category',
            'subcategory'
        ]
