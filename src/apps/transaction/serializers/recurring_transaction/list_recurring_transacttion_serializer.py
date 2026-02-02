from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import RecurringTransactionModel


class ListRecurringTransactionSerializer(serializers.ModelSerializer):
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
            'frequency',
            'next_run_date',
            'active',
            'init_date',
            'account',
            'category',
            'subcategory'
        ]
