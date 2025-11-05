from rest_framework import serializers

from apps.transaction.models import TransactionModel


class ViewTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = ('__all__',)
