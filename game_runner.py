from deck import Deck, Card
from player import Player

class Game_State:
	def __init__(self, num_players):
		self.play_deck = Deck(num_players)
		self.goal_deck = Deck(num_players, is_goal_deck=True)
		self.num_players = num_players
		self.players = []
		for i in range(num_players):
			player_name = input(f"Please enter the name for player {i + 1}: ")
			self.players.append(Player(player_name, i))
	
	def run_round(self):
		self.setup_players()
		self.setup_goals(3)
		self.do_goal_selection()

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
		while self.goals:
			curr_player = self.players[curr_player_num]
			goal_num = input(f"Its {curr_player.name}'s turn to pick a goal: \n {[str(i + 1) + ": " + str(c) for i, c in enumerate(self.goals)]}\n")
			if not goal_num.isnumeric() or int(goal_num) < 1 or int(goal_num) > len(self.goals):
				print(f"Invalid choice! Enter a number between 1 and {len(self.goals)}")
			else:
				goal_num = int(goal_num)
				curr_player.take_goal(self.goals[goal_num - 1])
				self.goals.pop(goal_num - 1)
				curr_player_num = (curr_player_num + 1) % self.num_players
	
	def play_round(self):
		pass


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