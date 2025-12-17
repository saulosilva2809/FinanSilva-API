from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransactionModel


class DetailTransactionSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer()
    category = BaseMiniSerializer()
    subcategory = BaseMiniSerializer()

    class Meta:
        model = TransactionModel
        fields = [
            'id',
            'created_at',
            'updated_at',
            'type_transaction',
            'value',
            'account',
            'category',
            'subcategory',
            'recurring_root',
        ]
