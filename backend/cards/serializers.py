from rest_framework import serializers
from .models import Card, Booster


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "small_image",
            "large_image",
            "rarity",
        ]


class BoosterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booster
        fields = [
            "name",
            "image",
        ]
