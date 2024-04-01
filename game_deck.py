from itertools import repeat
import random
from numpy import array_split

class Deck:
	deck = []
	num_players = 4
	def __init__(self, num_players):
		self.generate_deck()
		self.num_players = num_players

	def generate_deck(self):
		colors = ["R", "B", "Y"]
		if self.num_players > 3:
			colors.append("G")
		nums = list(range(1, 10))
		for c in colors:
			self.deck.extend(zip(repeat(c), nums))
		self.deck.extend(zip(repeat("T"), range(1, 5)))

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		hands = array_split(self.deck, self.num_players)
		return hands

	def __str__(self):
		s = ""
		for card in self.deck:
			s = s + card[0] + " " + str(card[1]) + "\n"
		s.strip()
		return s