from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransactionModel


class ListTransactionSerializer(serializers.ModelSerializer):
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
    recurring_root = BaseMiniSerializer({"id": serializers.UUIDField()})
    transfer_root = BaseMiniSerializer({"id": serializers.UUIDField()})

    class Meta:
        model = TransactionModel
        fields = [
            'id',
            'value',
            'type_transaction',
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'transfer_root',
        ]
