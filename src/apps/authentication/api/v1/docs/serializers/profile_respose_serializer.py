from rest_framework import serializers


class ProfileResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %H:%M:%S')
