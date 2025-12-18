from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransactionModel


class ListTransactionSerializer(serializers.ModelSerializer):
    account = BaseMiniSerializer()
    category = BaseMiniSerializer()
    subcategory = BaseMiniSerializer()

    class Meta:
        model = TransactionModel
        fields = [
            'id',
            'value',
            'type_transaction',
            'account',
            'category',
            'subcategory',
        ]
