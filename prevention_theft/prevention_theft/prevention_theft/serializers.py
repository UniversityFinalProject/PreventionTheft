from rest_framework import serializers
from . import models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = (
            "name",
            "disappeared_time",
            "disappeared_count",
            "link",
        )
