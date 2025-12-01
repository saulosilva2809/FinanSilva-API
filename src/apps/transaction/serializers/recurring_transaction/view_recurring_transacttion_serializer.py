from rest_framework import serializers

from apps.transaction.models import RecurringTransactionModel


class ViewRecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransactionModel
        fields = '__all__'
