from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import RecurringTransactionModel


class ListRecurringTransactionSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer()
    category = BaseMiniSerializer()
    subcategory = BaseMiniSerializer()

    class Meta:
        model = RecurringTransactionModel
        fields = [
            'id',
            'value',
            'type_transaction',
            'next_run_date',
            'active',
            'account',
            'category',
            'subcategory'
        ]
