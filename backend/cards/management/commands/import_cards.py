"""
Import all card from API to the database.
"""
import json
import requests
import tempfile
from tqdm import tqdm
from datetime import datetime
from django.core import files
from cards.models import Card as dbCard
from cards.models import Set as dbSet
from pokemontcgsdk import RestClient, Card, Set
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

        parser.add_argument(
            "--clean-db",
            action="store_true",
            help="Remove all card in database",
        )

    def handle(self, *args, **options):
        start = datetime.now()
        if options["clean_db"]:
            logger.info("Remove old card")
            dbCard.objects.all().delete()

        # get config file
        with open("cards/config.json", "r") as f:
            config = json.load(f)

        for _id, _data in config["extensions"].items():
            # Collect the set detail
            set_data = Set.find(_id)
            set_obj = dbSet(
                name=set_data.name,
                series=set_data.series,
                release_date=datetime.strptime(
                    set_data.releaseDate, "%Y/%m/%d"),
                extension_id=set_data.id
                )
            # Download set symbol
            symbol = self.download_image(
                set_data.images.symbol, not options["no_ssl_verification"])
            if symbol is not None:
                set_obj.symbol.save(_id + ".png", symbol)

            # Download set Logo
            logo = self.download_image(
                set_data.images.logo, not options["no_ssl_verification"])
            if logo is not None:
                set_obj.logo.save(_id + ".png", logo)

            set_obj.save()
            # Collect card:
            cards = Card.where(q=f"set.id:{_id}")
            for card in tqdm(cards):
                c = dbCard(
                    name=card.name, rarity=card.rarity,
                    subType=card.subtypes, type=card.types,
                    superType=card.supertype, number=card.number
                )
                small = self.download_image(
                    card.images.small, not options["no_ssl_verification"])
                if small is not None:
                    c.small_image.save(card.name + "_small.png", small)
                large = self.download_image(
                    card.images.large, not options["no_ssl_verification"])

                if large is not None:
                    c.large_image.save(card.name + "_large.png", large)

                # Define if the card is holo or not
                c.holo_type = "H" if _data["rarity"][c.rarity]["holo"] else "N"

                # Add the extension to the item
                c.extension_id = _id

                # Save the card object
                c.save()

        end = datetime.now()
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
        except Exception as e:
            logger.warn("Cannot download image")
            logger.warn(e)
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
