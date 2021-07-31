# Module is meant to act as an interface to the mtgsdk library

from mtgsdk import Card
# from mtgsdk import Set
# from mtgsdk import Type


# Variables
COMMON = 'Common'
UNCOMMON = 'Uncommon'
RARE = 'Rare'
MYTHIC = 'Mythic Rare'


def fetch_by_name(name):
	print(name)
	cards = Card.where(name=name).all()
	cards.sort(key=lambda x: x.name)
	return cards


def fetch_by_id(mv_id):
	print(id)
	card = Card.find(mv_id)
	return card
