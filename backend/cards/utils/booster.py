from cards.models import Card
from random import choice, randint


def generate_booster(extension_id, extension_data):
    """
    With an extension id generate a booster (a list of card) selected
    """

    # Get card of that extension
    extension_card = Card.objects.filter(extension_id=extension_id)
    booster_composition = []
    for card_rarity_possibility in extension_data["booster"]:
        if len(card_rarity_possibility) == 1:
            rarity = card_rarity_possibility[0]
            booster_composition.append(
                choice(list(extension_card.filter(rarity=rarity)))
            )
        else:
            luck = randint(0, 100)
            actual_rate = 0
            for rarity in card_rarity_possibility[:-1]:
                rarity_rate = extension_data["rarity"][rarity]["rate"]
                if luck <= actual_rate + rarity_rate:
                    selected_rarity = rarity
                    break
                else:
                    actual_rate += rarity_rate
            else:
                selected_rarity = card_rarity_possibility[-1]
            booster_composition.append(
                choice(list(extension_card.filter(rarity=selected_rarity)))
            )
    return booster_composition
