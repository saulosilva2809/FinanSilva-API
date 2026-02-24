from rest_framework import serializers

from apps.account.models import AccountModel


class ViewAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = ('id', 'name', 'bank', 'type_account', 'description', 'initial_balance', 'balance')
