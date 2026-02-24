from rest_framework import serializers

from apps.base.serializer import BaseMiniSerializer
from apps.transaction.models import TransferModel


class ListTransferSerializer(serializers.ModelSerializer):
    original_account = BaseMiniSerializer({
        "id": serializers.UUIDField(),
        "name": serializers.CharField()
    })
    account_transferred = BaseMiniSerializer({
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
        model = TransferModel
        fields = [
            'id',
            'value',
            'original_account',
            'account_transferred',
            'category',
            'subcategory',
        ]
