from rest_framework import serializers
from .models import Details_Table
class DataSerializer(serializers.Serializer):
    name = serializers.CharField()
    latitude = serializers.CharField()
    longitude = serializers.CharField()
    location = serializers.CharField()
    urls = serializers.CharField()
    rating = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.

        """
        return Details_Table.objects.create(**validated_data)

