from rest_framework import serializers
from .models import Card, Set, UsersBooster


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "name",
            "small_image",
            "large_image",
            "rarity",
            "holo_type",
        ]


class BoosterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Set
        fields = [
            "name",
            "logo",
            "symbol"
        ]


class UsersBoosterSerializer(serializers.HyperlinkedModelSerializer):

    booster_id = serializers.CharField(source="booster.extension_id")
    logo = serializers.CharField(source="booster.logo")
    symbol = serializers.CharField(source="booster.symbol")

    class Meta:
        model = UsersBooster
        fields = [
            "booster_id",
            "logo",
            "symbol",
            "number",
        ]
