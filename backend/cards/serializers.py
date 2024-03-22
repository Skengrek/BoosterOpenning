from rest_framework import serializers
from .models import Card, Set, Booster


class CardSerializer(serializers.HyperlinkedModelSerializer):
    has_it = serializers.SerializerMethodField(required=False)
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
            "has_it",
        ]

    def __init__(self, data, user=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.user = user

    def get_has_it(self, obj):
        if self.user is not None:
            return not self.user.card_set.filter(id=obj.id).exists()
        return True


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
