"""
Import all card from API to the database.
"""

import requests
import tempfile
from datetime import datetime
from urllib.parse import urlparse
from django.core import files
from cards.models import Card as dbCard
from pokemontcgsdk import RestClient, Card
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand


RestClient.configure("2edc305c-9242-4cd2-8006-824a746f9120")


class Command(BaseCommand):
    help = "Import all cards"

    def handle(self, *args, **options):
        start = datetime.now()

        print("Remove old card")
        dbCard.objects.all().delete()
        cards = Card.where(q="set.id:swsh12")
        print(len(cards))

        # cards = Card.all()
        end = datetime.now()
        new_card = []
        for card in cards:
            c = dbCard(name=card.name, rarity=card.rarity)
            small = self.download_image(card.images.small)
            if small is not None:
                c.small_image.save(card.name + "_small.png", small)
            large = self.download_image(card.images.large)
            if large is not None:
                c.large_image.save(card.name + "_large.png", large)
            c.save()
        print(end - start)

    @staticmethod
    def download_image(image_url):
        try:
            # Stream the image from the url
            response = requests.get(image_url, stream=True)

            # Was the request OK?
            if response.status_code != requests.codes.ok:
                # Nope, error handling, skip file etc etc etc
                return
        except:
            return None

        # Create a temporary file
        lf = tempfile.NamedTemporaryFile()

        # Read the streamed image in sections
        for block in response.iter_content(1024 * 8):

            # If no more file then stop
            if not block:
                break

            # Write image block to temporary file
            lf.write(block)
        return files.File(lf)
