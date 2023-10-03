from rest_framework import serializers
from .models import Card, Set, Booster


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "number",
            "small_image",
            "large_image",
            "rarity",
            "holo_type",
        ]


class BoosterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Set
        fields = ["name", "logo", "symbol"]


class UsersBoosterSerializer(serializers.HyperlinkedModelSerializer):
    booster_id = serializers.CharField(source="set.extension_id")
    logo = serializers.CharField(source="set.logo")
    symbol = serializers.CharField(source="set.symbol")

    class Meta:
        model = Booster
        fields = [
            "booster_id",
            "logo",
            "symbol",
            "number",
        ]
