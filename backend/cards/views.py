import json
from cards.models import Card, Booster
from cards.serializers import CardSerializer, BoosterSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from random import choice
from cards.utils.booster import generate_booster

# Create your views here.


def cardsListing(request):
    """List all lists"""
    if request.method == "GET":
        lists = Card.objects.all()
        serializer = CardSerializer(lists, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)


def cardDetails(request, pk):
    try:
        _list = Card.objects.get(pk=pk)
    except Card.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = CardSerializer(_list, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)

    elif request.method == "DELETE":
        # delete the task
        _list.delete()
        # return a no content response.
        return HttpResponse(status=204)


def random_booster(request):
    """
    Generate a booster. If no extension id is given, then create a random one.
    Rarity and rates of cards and booster composition are define in a
    config.json file

    Args:
        request: the Request that lead to hear
        extension_id: the id of an extension to generate a booster for.
    """
    if request.method == "GET":
        # Read config:
        # get config file
        with open("cards/config.json", "r") as f:
            config = json.load(f)
        # Select a random extension
        extension_key = choice(list(config["extensions"].keys()))

        card_in_booster = generate_booster(extension_key, config["extensions"][extension_key])

        # Booster
        booster = Booster.objects.get(name="test")

        # Serializers
        cards = CardSerializer(card_in_booster, many=True)
        boosterJson = BoosterSerializer(booster)

        # JSON Data
        jsonData = {"cards": cards.data, "booster": boosterJson.data}
        return JsonResponse(jsonData, safe=False)
