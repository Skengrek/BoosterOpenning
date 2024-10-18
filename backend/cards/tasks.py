import os
import dotenv
import requests
import tempfile
from datetime import datetime
from django.core import files
from celery import shared_task
from cards.models import CardRarity
from cards.models import Card as dbCard
from cards.models import Set as dbSet
from pokemontcgsdk import RestClient, Card, Set



from logging import getLogger

dotenv.load_dotenv()
logger = getLogger(__name__)
RestClient.configure(os.environ.get("POKEMON_TCG_API_KEY"))

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
        logger.warning("Cannot download image")
        logger.warning(e)
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


@shared_task
def import_set_task(set_extension_id, ssl_verification=False):
    logger.info(f"Start importing {set_extension_id}")
    RestClient.configure(os.environ.get("POKEMON_TCG_API_KEY"))

    # Import set data
    
    already_imported_set = dbSet.objects.values_list('extension_id', flat=True)
    if set_extension_id in already_imported_set:
        raise Exception("Set already exist")
    set_data = Set.find(set_extension_id)
    set_obj = dbSet(
        name=set_data.name,
        series=set_data.series,
        release_date=datetime.strptime(
            set_data.releaseDate, "%Y/%m/%d"),
        extension_id=set_data.id
        )
    # Download set symbol
    symbol = download_image(
        set_data.images.symbol, not ssl_verification)
    if symbol is not None:
        set_obj.symbol.save(set_extension_id + ".png", symbol)

    # Download set Logo
    logo = download_image(
        set_data.images.logo, not ssl_verification)
    if logo is not None:
        set_obj.logo.save(set_extension_id + ".png", logo)

    set_obj.save()
        
    logger.info("Set imported")
    imported_data = []
    cards = Card.where(q=f"set.id:{set_extension_id}")
    logger.info(type(cards))
    
    for index, card in enumerate(cards):
        logger.info(f"{card.name}")
        logger.info(f"{card.rarity}")
        try: 
            rarity_obj = CardRarity.objects.get(name=card.rarity, set=set_obj)
        except CardRarity.DoesNotExist:
            rarity_obj = CardRarity(
                holo=False,
                name=card.rarity,
                rate=1,
                set=set_obj
            )
            rarity_obj.save()
        c = dbCard(
            name=card.name, rarity=rarity_obj,
            subType=card.subtypes, type=card.types,
            superType=card.supertype, number=card.number
        )
        small = download_image(
            card.images.small,
            not ssl_verification
        )
        if small is not None:
            c.small_image.save(card.name + "_small.png", small)
        large = download_image(
            card.images.large,
            not ssl_verification
        )

        if large is not None:
            c.large_image.save(card.name + "_large.png", large)

        # Add the extension to the item
        c.extension_id = set_extension_id

        # Save the card object
        c.save()
        import_set_task.update_state(state='PROGRESS', meta={'current': index + 1, 'total': len(cards)})
    return {'data': imported_data, 'total': len(cards)}
