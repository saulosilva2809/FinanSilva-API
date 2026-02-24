from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransactionModel


class DetailTransactionSerializer(serializers.ModelSerializer):
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
    transfer_root = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "original_account": serializers.CharField(),
        "account_transferred": serializers.CharField()
    })
    is_transfer = serializers.SerializerMethodField()

    class Meta:
        model = TransactionModel
        fields = [
            'id',
            'created_at',
            'updated_at',
            'value',
            'type_transaction',
            'description',
            'account',
            'category',
            'subcategory',
            'recurring_root',
            'is_transfer',
            'transfer_root',
        ]

    def get_is_transfer(self, obj):
        return obj.transfer_root is not None
