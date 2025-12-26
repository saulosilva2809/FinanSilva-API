from rest_framework import serializers


class BaseMiniSerializer(serializers.Serializer):
    def __init__(self, fields: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field_instance in fields.items():
            self.fields[field_name] = field_instance
