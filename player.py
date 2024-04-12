import random
from cards import Card

class Player:
    def __init__(self, name) -> None:
        self.hand = []
        self.name = name

    def set_hand(self, hand):
        self.hand = hand

    def draw_card(self, card):
        self.hand.append(card)
    
    def draw_cards(self, cards):
        self.hand.extend(cards)

    def play_top_card(self):
        if self.hand:
            return self.hand.pop(0)
        return None
    
    def num_cards(self):
        return len(self.hand)
    
    def sort_hand(self):
        self.hand.sort()
    
    def clear_hand(self):
        self.hand = []

    def hand_str(self):
        return " ".join([str(c) for c in self.hand])
    
    def has_suit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False
    
    def play_card(self, card):
        self.hand.remove(card)
        return card

