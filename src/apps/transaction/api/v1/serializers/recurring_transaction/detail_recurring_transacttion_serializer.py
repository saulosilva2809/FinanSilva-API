from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import RecurringTransactionModel


class DetailRecurringTransactionSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    category = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    subcategory = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })

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
            'account',
            'category',
            'subcategory'
        ]
