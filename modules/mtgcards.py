# Module is meant to act as an interface to the mtgsdk library

from mtgsdk import Card

# from mtgsdk import Set
# from mtgsdk import Type


# Variables
COMMON = 'Common'
UNCOMMON = 'Uncommon'
RARE = 'Rare'
MYTHIC = 'Mythic Rare'


class CustomCardData:
	def __init__(self, name=None, multiverseid=None, setname=None, ctype=None, csubtype=None,
				 colorid=None, manacost=None, foil=False):
		self.name = name
		self.multiverseId = multiverseid
		self.setName = setname
		self.type = ctype
		self.subtype = csubtype
		self.colorId = colorid
		self.manaCost = manacost
		self.foil = foil


def fetch_by_name(name):
	print(name)
	cards = Card.where(name=name).all()
	cards.sort(key=lambda x: x.name)
	return cards


def fetch_by_id(mv_id):
	card = Card.find(mv_id)
	return card


def stringify_color_id(card):
	if card.color_identity is None:
		return "NULL"
	else:
		colorid = ""
		for color in card.color_identity:
			colorid = colorid + color
		return colorid