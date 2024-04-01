import game_deck

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
	# Select players

	num_players = 4
	deck = game_deck.Deck(num_players)
	deck.shuffle()
	hands = deck.deal()
	while True:
		for hand in hands:
			player_turn(hand)
		continue

def player_turn(hand):
	while True:
		command = input("Enter a command: ").split()
		match command:
			case ["help"]:
				print("Options:\n\tlist hand\n\tplay card")
			case ["list", "hand"]:
				print(hand)
			case ["play", _]:
				print(command)
			case _:
				print("Invalid Command.")
		continue

def validate_num_players(value):
	return value > 2 and value < 6

if __name__ == "__main__":
	run_game()
	
