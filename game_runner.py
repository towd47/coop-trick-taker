import copy
from deck import Deck, Card
from player import Player

class Game_State:
	def __init__(self, num_players):
		self.play_deck = Deck(num_players)
		self.goal_deck = Deck(num_players, is_goal_deck=True)
		self.num_players = num_players
		self.players = []
		self.stack = []
		for i in range(num_players):
			player_name = input(f"Please enter the name for player {i + 1}: ")
			self.players.append(Player(player_name, i))
	
	def run_round(self):
		self.setup_players()
		self.setup_goals()
		self.do_goal_selection()
		self.play_round()

	def setup_players(self):
		self.play_deck.shuffle()
		hands = self.play_deck.deal_hands()
		for player, hand in zip(self.players, hands):
			player.set_hand(hand)

		for player in self.players:
			if player.is_captain():
				self.captain = player.position

	def setup_goals(self):
		self.goal_deck.shuffle()
		self.goals = self.goal_deck.deal_goals(3)

	def do_goal_selection(self):
		curr_player_num = self.captain
		remaining_goals = copy.deepcopy(self.goals)
		while remaining_goals:
			curr_player = self.players[curr_player_num]
			goal_num = input(f"Its {curr_player.name}'s turn to pick a goal: \n {[str(i + 1) + ": " + str(c) for i, c in enumerate(remaining_goals)]}\n")
			if not goal_num.isnumeric() or int(goal_num) < 1 or int(goal_num) > len(remaining_goals):
				print(f"Invalid choice! Enter a number between 1 and {len(remaining_goals)}")
			else:
				goal_num = int(goal_num)
				curr_player.take_goal(remaining_goals[goal_num - 1])
				remaining_goals.pop(goal_num - 1)
				curr_player_num = (curr_player_num + 1) % self.num_players
	
	def play_round(self):
		lead_player = self.captain
		while self.goals or self.players[0].hand:
			lead_player = self.play_hand(lead_player)
			for play in self.stack:
				if play[0] in self.goals:
					self.check_goal(play[0])

	def check_goal(self, card):
		return True

	def play_hand(self, curr_player_num):
		self.stack = []
		self.led_suit = None
		for i in range(self.num_players):
			curr_player_num = (curr_player_num + i) % self.num_players
			curr_player = self.players[curr_player_num]
			card = self.request_card(curr_player, self.led_suit)
			self.stack.append((card, curr_player_num))
			if not self.led_suit:
				self.led_suit = card.suit
			curr_player.play_card(card)
		return self.get_winner()
	
	def get_winner(self):
		cards, _ = list(zip(*self.stack))
		cards = [card for card in cards if card.suit == self.led_suit or card.suit == "T"]
		high_card = max(cards)
		for play in self.stack:
			if play[0] == high_card:
				print(f"{self.players[play[1]].name} took the trick with {str(play[0])}")
				return play[1]
		return -1

	def request_card(self, player, suit):
		valid_card = False
		if not suit or not player.has_suit(suit):
			suit = None
		while not valid_card:
			card_choice = input(f"Its {player.name}'s turn to play. Your hand is {Deck.hand_string(player.hand)}\n")
			card_choice = Card(card_choice[0], card_choice[1])
			valid_card = card_choice in player.hand and (not suit or card_choice.suit == suit)
		return card_choice

def run_game():
	got_players = False
	while not got_players:
		num_players = input("Select num players (3-5): ")
		try:
			num_players = int(num_players)
			got_players = validate_num_players(num_players)
			if not got_players:
				print("input outside range 3-5")
		except:
			print("Invalid input")

	game_state = Game_State(num_players)
	game_state.run_round()

def validate_num_players(value):
	return value > 2 and value < 6