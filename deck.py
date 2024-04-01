from itertools import repeat
import random
from numpy import array_split

class Deck:
	def __init__(self, num_players, is_goal_deck = False):
		self.num_players = num_players
		self.generate_deck(is_goal_deck)

	def generate_deck(self, is_goal_deck):
		self.deck = []
		suits = ["R", "B", "Y"]
		if self.num_players > 3:
			suits.append("G")
		nums = list(range(1, 10))
		for s in suits:
			for n in nums:
				self.deck.append(Card(s, str(n)))
		if not is_goal_deck:
			start = 1
			if self.num_players == 3:
				start = 2
			for n in range(start, 5):
				self.deck.append(Card("T", str(n)))

	def shuffle(self):
		random.shuffle(self.deck)

	def deal_hands(self):
		hands = array_split(self.deck, self.num_players)
		return hands
	
	def deal_goals(self, num_goals):
		num_goals = min(num_goals, len(self.deck))
		num_goals = max(1, num_goals)		
		return self.deck[:num_goals]

	def __str__(self):
		s = "\n".join([str(card) for card in self.deck])
		return s
	
	def print_hand(hand):
		print(",".join(str(card) for card in hand))

class Card:
	def __init__(self, suit, num):
		self.suit = suit
		self.num = num

	def __eq__(self, card):
		if self.suit == card.suit and self.num == card.num:
			return True
		return False
	
	def __str__(self):
		return self.suit + self.num
	
	def is_captain_card(self):
		return self.suit == "T" and self.num == "4"