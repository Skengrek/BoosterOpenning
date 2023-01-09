from cards.models import Card, Booster
from cards.serializers import CardSerializer, BoosterSerializer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

from random import randint

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


def booster(request):
    """
    Card rarity:
    Common, Uncommon, Rare, Rare Holo, Rare Holo V, Rare Rainbow, Rare Secret

    a booster:
    6 Common, 3 Uncommon, 1 Rare and +

    Selection of rare and +:
    Rare: 35%
    Rare holo: 30%
    Rare Holo V: 20%
    Rare Rainbow: 10%
    Rare Secret: 5%
    """
    all_card = Card.objects.all()
    commons = all_card.filter(rarity="Common")
    uncommons = all_card.filter(rarity="Uncommon")
    rare = all_card.filter(rarity="Rare")
    rareholo = all_card.filter(rarity="Rare Holo")
    rareholoV = all_card.filter(rarity="Rare Holo V")
    rarerainbow = all_card.filter(rarity="Rare Rainbow")
    raresecret = all_card.filter(rarity="Rare Secret")

    if request.method == "GET":
        #  Generate a booster
        card_in_booster = []
        # 6 Common cards
        nb_common = len(commons)
        for _ in range(6):
            card_in_booster.append(commons[randint(0, nb_common - 1)])

        # 3 Uncommon
        nb_uncommon = len(uncommons)
        for _ in range(3):
            card_in_booster.append(uncommons[randint(0, nb_uncommon - 1)])

        # The rare case
        luck = randint(0, 100)
        if 0 < luck < 35:
            card_in_booster.append(rare[randint(0, len(rare) - 1)])
        elif 35 <= luck < 65:
            card_in_booster.append(rareholo[randint(0, len(rareholo) - 1)])
        elif 65 <= luck < 85:
            card_in_booster.append(rareholoV[randint(0, len(rareholoV) - 1)])
        elif 85 <= luck < 95:
            card_in_booster.append(rarerainbow[randint(0, len(rarerainbow) - 1)])
        else:
            card_in_booster.append(raresecret[randint(0, len(raresecret) - 1)])

        # Booster
        booster = Booster.objects.get(name="Silver Tempest")

        # Serializers
        cards = CardSerializer(card_in_booster, many=True)
        boosterJson = BoosterSerializer(booster)

        # JSON Data
        jsonData = {"cards": cards.data, "booster": boosterJson.data}
        return JsonResponse(jsonData, safe=False)
