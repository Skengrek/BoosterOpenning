"""
Import all card from API to the database.
"""
from pokemontcgsdk import RestClient, Card, Set
from django.core.management.base import BaseCommand


from logging import getLogger
logger = getLogger(__name__)
RestClient.configure("2edc305c-9242-4cd2-8006-824a746f9120")


class Command(BaseCommand):
    help = "Import all cards"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            action="store",
            help="Enter the set id you want the list of rarity",
        )

    def handle(self, *args, **options):
        # If no set is given, list all ids
        if not options["s"]:
            for s in Set.all():
                print(s.id)
            return None
        
        rarity = []
        for c in Card.where(q=f"set.id:{options['s']}"):
            if c.rarity not in rarity:
                rarity.append(c.rarity)
        print(rarity)
