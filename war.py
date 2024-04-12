import pygame
from enum import Enum
import random
from playing_cards import PlayingCardDeck
from cards import Pile
from player import Player

class WarGameState(Enum):
    PLAYING = 0
    COMPARING = 1
    TIED = 2
    RESOLVING = 3
    REVEALING = 4
    ENDED = 5

class WarEngine:
    def __init__(self) -> None:
        self.players = []
        self.piles = []
        self.winner = None
        for i in range(2):
            self.players.append(WarPlayer(f"Player_{str(i)}"))
            self.piles.append(Pile())
        self._setup_deck()
        self._deal_deck()
        self.game_state = WarGameState.PLAYING

    def _setup_deck(self):
        self.deck = PlayingCardDeck()
        self.deck.shuffle()

    def _deal_deck(self):
        hands = self.deck.deal_deck(2, overflow=True)
        for player, hand in zip(self.players, hands):
            player.set_hand(hand)

    def flip_cards(self):
        for player, pile in zip(self.players, self.piles):
            if player.num_cards() > 0:
                pile.add(player.play_top_card())
    
    def reveal(self):
        for pile in self.piles:
            for card in pile.stack:
                card.flip_faceup()
        self.game_state = WarGameState.RESOLVING

    def resolve_round(self, player_num):
        for pile in self.piles:
            self.players[player_num].discard_cards(pile.get_all())
            pile.clear()
        self.check_for_end()

    def check_for_end(self):
        for player in self.players:
            if player.num_cards() == 0:
                self.game_state = WarGameState.ENDED
    
    def compare_cards(self):
        self.winner = 0
        if self.piles[1].stack[-1].higher_than(self.piles[0].stack[-1]):
            self.winner = 1
            if len(self.piles[0].stack) > 1 or len(self.piles[1].stack) > 1:
                self.game_state = WarGameState.COMPARING
            else:
                self.game_state = WarGameState.RESOLVING
        elif self.piles[0].stack[-1].equals(self.piles[1].stack[-1]):
            self.game_state = WarGameState.TIED
        else:
            if len(self.piles[0].stack) > 1 or len(self.piles[1].stack) > 1:
                self.game_state = WarGameState.COMPARING
            else:
                self.game_state = WarGameState.RESOLVING
    
    def play(self, key):
        if key == None:
            return
        
        if self.game_state == WarGameState.ENDED:
            return
        
        if key == pygame.K_SPACE or key == pygame.MOUSEBUTTONUP:
            self.flip_cards()
            self.compare_cards()

    def step(self, key):
        if key == None:
            return
        
        if self.game_state == WarGameState.ENDED:
            return
        
        if key == pygame.K_SPACE or key == pygame.MOUSEBUTTONUP:
            if self.game_state == WarGameState.RESOLVING:
                self.resolve_round(self.winner)
                if self.game_state != WarGameState.ENDED:
                    self.game_state = WarGameState.PLAYING
            elif self.game_state == WarGameState.TIED:
                self.burn_tied_cards()
                self.game_state = WarGameState.PLAYING
            elif self.game_state == WarGameState.COMPARING:
                self.reveal()
                self.game_state = WarGameState.RESOLVING

    def burn_tied_cards(self):
        for player, pile in zip(self.players, self.piles):
            for _ in range(3):
                if player.num_cards() > 1:
                    card = player.play_top_card()
                    card.flip_facedown()
                    pile.add(card)

    def reset(self):
        for player in self.players:
            player.clear()
        self._setup_deck()
        self._deal_deck()
        self.game_state = WarGameState.PLAYING

    def get_players(self):
        return self.players

class WarPlayer(Player):
    def __init__(self, name) -> None:
        Player.__init__(self, name)
        self.discard = []

    def discard_card(self, card):
        self.discard.append(card)
    
    def discard_cards(self, cards):
        self.discard.extend(cards)

    def play_top_card(self):
        card = Player.play_top_card(self)
        if not card:
            random.shuffle(self.discard)
            self.draw_cards(self.discard)
            self.discard = []
            card = Player.play_top_card(self)
        return card
    
    def get_top_discard(self):
        if not self.discard:
            return None
        return self.discard[-1]
    
    def num_cards(self):
        return len(self.hand) + len(self.discard)
    
    def num_discard(self):
        return len(self.discard)
    
    def clear(self):
        self.hand = []
        self.discard = []

    def hand_str(self):
        return " ".join([str(c) for c in self.hand])
    
if __name__ == "__main__":
    game = WarEngine()
    for p in game.players:
        print(p.hand_str())
        input()
        p.hand.sort()
        print(p.hand_str())
        input()

        for i, c in enumerate(p.hand):
            print(c, p.hand[i + 1])
            print(c > p.hand[i + 1])
            input()

