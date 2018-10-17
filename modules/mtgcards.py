# Module is meant to act as an interface to the mtgsdk library

from mtgsdk import Card
# from mtgsdk import Set
# from mtgsdk import Type


# Variables
COMMON = 'Common'
UNCOMMON = 'Uncommon'
RARE = 'Rare'
MYTHIC = 'Mythic Rare'


def fetch(name):
    return Card.where(name=name).all()
