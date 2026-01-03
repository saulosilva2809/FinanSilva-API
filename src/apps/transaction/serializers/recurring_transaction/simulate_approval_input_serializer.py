from rest_framework import serializers


class SimulateApprovalInputSerializer(serializers.Serializer):
    reference_date = serializers.DateTimeField(required=False, allow_null=True)
