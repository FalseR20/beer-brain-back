from rest_framework import serializers


class CommonEventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    data = serializers.DateField()
    description = serializers.CharField(max_length=256)
    is_closed = serializers.BooleanField()
    members_count = serializers.IntegerField()

