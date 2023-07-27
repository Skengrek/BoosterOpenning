import json
from cards.models import Card, Booster
from cards.serializers import CardSerializer, BoosterSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from random import choice
from cards.utils.booster import generate_booster

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CardListing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lists = Card.objects.all()
        serializer = CardSerializer(lists, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)
        

class CardDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_list(pk):
        try:
            return Card.objects.get(pk=pk)
        except Card.DoesNotExist:
            return None
    def put(self, request, pk):
        _list = self.get_list(pk)
        if _list is None:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = CardSerializer(_list, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)
    
    def delete(self, request, pk):
        _list = self.get_list(pk)
        if _list is None:
            return HttpResponse(status=404)
        _list.delete()
        # return a no content response.
        return HttpResponse(status=204)


class RandomBooster(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Generate a booster. If no extension id is given, then create a random
        one.
        Rarity and rates of cards and booster composition are define in a
        config.json file

        Args:
            request: the Request that lead to hear
            extension_id: the id of an extension to generate a booster for.
        """
        # Read config:
        # get config file
        with open("cards/config.json", "r") as f:
            config = json.load(f)
        # Select a random extension
        extension_key = choice(list(config["extensions"].keys()))

        card_in_booster = generate_booster(
            extension_key, config["extensions"][extension_key]
        )

        # Booster
        booster = Booster.objects.get(name="test")

        # Serializers
        cards = CardSerializer(card_in_booster, many=True)
        boosterJson = BoosterSerializer(booster)

        # JSON Data
        jsonData = {"cards": cards.data, "booster": boosterJson.data}
        return JsonResponse(jsonData, safe=False)

