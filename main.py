import pygame
from war_runner import run_war
from util import load_keybinds

def render_menu_text(window):
	font = pygame.font.Font(None, 100)
	text = font.render("Card Games R Here", True, "black")
	window.blit(text, (window.get_rect().width / 2 - text.get_rect().width / 2, 150))

if __name__ == "__main__":
	keybinds = load_keybinds()
	pygame.init()
	bounds = (1024, 768)
	window = pygame.display.set_mode(bounds)
	pygame.display.set_caption("Cards Games")
	button = pygame.Rect(window.get_rect().width / 2 - 75, 500, 150, 50)
	font = pygame.font.Font(None, 50)
	buttonText = font.render("War", True, "black")

	running = True
	while running:
		window.fill((53,101,77))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				if button.collidepoint(pos):
					run_war()

		render_menu_text(window)
		pygame.draw.rect(window, "red", button)
		window.blit(buttonText, (button.centerx - buttonText.get_rect().width / 2, button.centery - buttonText.get_rect().height / 2))
		pygame.display.update()