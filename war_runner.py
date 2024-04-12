import sys
import pygame
from war import WarEngine, WarGameState

CARD_SCALE = .7
card_back = pygame.image.load("images/1B.png")
card_back = pygame.transform.scale(card_back, (int(238 * CARD_SCALE), int(332 * CARD_SCALE)))

def renderGame(window, warEngine):
	window.fill((53,101,77))
	font = pygame.font.SysFont('comicsans', 60, True)

	players = warEngine.get_players()

	window.blit(card_back, (100, 250))
	window.blit(card_back, (740, 250))

	text = font.render(str(len(players[0].hand)) + " cards", True, (255,255,255))
	window.blit(text, (60, 500))

	text = font.render(str(len(players[1].hand)) + " cards", True, (255,255,255))
	window.blit(text, (700, 500))

	for i, card in enumerate(warEngine.piles[0].stack):
		if card.is_faceup():
			image = scaleImage(card.image)
		else:
			image = card_back
		window.blit(image, (300, 50 + (40 * i)))

	for i, card in enumerate(warEngine.piles[1].stack):
		if card.is_faceup():
			image = scaleImage(card.image)
		else:
			image = card_back
		window.blit(image, (550, 50 + (40 * i)))

	for i, player in enumerate(players):
		if player.discard:
			image = scaleImage(player.get_top_discard().image, .5)
			window.blit(image, (120 + (640 * i), 15))
			text = font.render(str(player.num_discard()) + " cards", True, (0, 0, 0))
			window.blit(text, (60 + (640 * i), 150))

	if warEngine.game_state == WarGameState.RESOLVING:
		if warEngine.winner == 0:
			text = font.render(">", True, (0,0,0))
		else:
			text = font.render("<", True, (0,0,0))
		window.blit(text, (490, 100))
	elif warEngine.game_state == WarGameState.TIED:
		text = font.render("=", True, (0, 0, 0))
		window.blit(text, (490, 100))
	elif warEngine.game_state == WarGameState.ENDED:
		text = font.render("Game Over", True, (0, 0, 0))
		text2 = font.render(f"Player {warEngine.winner + 1} Wins!", True, (0, 0, 0))
		window.blit(text, (350, 350))
		window.blit(text2, (350, 400))

def render_hand(window, hand, height):
	num_cards = len(hand)
	
	spacing = int(800 / max(num_cards, 1))
	for i, card in enumerate(hand):
		if card.is_faceup():
			image = scaleImage(card.image)
		else:
			image = card_back
		window.blit(image, (50 + (spacing * i), height))

def scaleImage(image, scale=CARD_SCALE):
	return pygame.transform.scale(image, (int(238 * scale), int(332 * scale)))

def run_war():
	bounds = (1024, 768)
	window = pygame.display.set_mode(bounds)
	pygame.display.set_caption("WAR")

	card_back = pygame.image.load("images/1B.png")
	card_back = pygame.transform.scale(card_back, (int(238 * CARD_SCALE), int(332 * CARD_SCALE)))

	warEngine = WarEngine()
	running = True
	accel = False

	font = pygame.font.Font(None, 50)
	button = pygame.Rect(0, 0, 25, 25)
	buttonText = font.render("X", True, "black")

	accel_key = pygame.K_f

	while running:
		key = None
		mouse_pos = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				key = event.key
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				mouse_pos = pos
				if button.collidepoint(pos):
					running = False

		if key == accel_key:
			accel = not accel

		if warEngine.game_state == WarGameState.ENDED:
			if key == pygame.K_r:
				warEngine.reset()
		else:
			if accel:
				pygame.time.delay(10)
				if warEngine.game_state == WarGameState.PLAYING:
					warEngine.play(pygame.K_SPACE)
				elif warEngine.game_state == WarGameState.RESOLVING or warEngine.game_state == WarGameState.TIED or warEngine.game_state == WarGameState.COMPARING:
					warEngine.step(pygame.K_SPACE)
			else:
				if warEngine.game_state == WarGameState.PLAYING:
					warEngine.play(key)
				elif warEngine.game_state == WarGameState.RESOLVING or warEngine.game_state == WarGameState.TIED or warEngine.game_state == WarGameState.COMPARING:
					warEngine.step(key)

		p1_pile = pygame.Rect(100, 250, card_back.get_width(), card_back.get_height())
		if mouse_pos and p1_pile.collidepoint(mouse_pos):
			if warEngine.game_state == WarGameState.PLAYING:
				warEngine.play(pygame.MOUSEBUTTONUP)
			elif warEngine.game_state == WarGameState.RESOLVING or warEngine.game_state == WarGameState.TIED or warEngine.game_state == WarGameState.COMPARING:
				warEngine.step(pygame.MOUSEBUTTONUP)

		renderGame(window, warEngine)
		render_hand(window, warEngine.players[0].hand, 700)
		pygame.draw.rect(window, "red", button)
		window.blit(buttonText, (button.centerx - buttonText.get_rect().width / 2, button.centery - buttonText.get_rect().height / 2))

		pygame.display.update()
