from rest_framework import serializers


class BaseMiniSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
