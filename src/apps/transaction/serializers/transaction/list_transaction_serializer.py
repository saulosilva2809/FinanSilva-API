from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransactionModel


class ListTransactionSerializer(serializers.ModelSerializer):
    category = BaseMiniSerializer()
    subcategory = BaseMiniSerializer()

    class Meta:
        model = TransactionModel
        fields = [
            'id',
            'type_transaction',
            'value',
            'category',
            'subcategory',
        ]
