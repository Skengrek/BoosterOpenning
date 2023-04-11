"""
Import all card from API to the database.
"""
import requests
import tempfile
from datetime import datetime
from django.core import files
from cards.models import Card as dbCard
from pokemontcgsdk import RestClient, Card
from django.core.management.base import BaseCommand

from logging import getLogger
logger = getLogger(__name__)
RestClient.configure("2edc305c-9242-4cd2-8006-824a746f9120")


class Command(BaseCommand):
    help = "Import all cards"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-ssl-verification",
            action="store_true",
            help="Do not use ssl verification for downloading images",
        )

    def handle(self, *args, **options):
        start = datetime.now()
        print("Remove old card")
        dbCard.objects.all().delete()
        cards = Card.where(q="set.id:swsh12")
        print(len(cards))
        end = datetime.now()
        for card in cards:
            c = dbCard(name=card.name, rarity=card.rarity,
                       subType=card.subtypes, type=card.types,
                       superType=card.supertype, number=card.number)
            small = self.download_image(card.images.small,
                                        not options["no_ssl_verification"])
            if small is not None:
                c.small_image.save(card.name + "_small.png", small)
            large = self.download_image(card.images.large,
                                        not options["no_ssl_verification"])
            if large is not None:
                c.large_image.save(card.name + "_large.png", large)
            c.save()
            print(f"Added {c.name}")
        print(end - start)

    @staticmethod
    def download_image(image_url, ssl_verification):
        try:
            # Stream the image from the url
            response = requests.get(image_url, stream=True,
                                    verify=ssl_verification)

            # Was the request OK?
            if response.status_code != requests.codes.ok:
                # Nope, error handling, skip file etc etc etc
                return
        except:
            logger.warn("Cannot download image")
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
