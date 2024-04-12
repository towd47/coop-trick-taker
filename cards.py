import random

class Deck:
    def __init__(self, include_jokers = False) -> None:
        self.deck = []
        self.card_back = None
    
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_deck(self, num_players, overflow = False):
        num_cards = int(len(self.deck) / num_players)
        hands = []
        for _ in range(num_players):
            hand = []
            for _ in range(num_cards):
                hand.append(self.deal_card())
            hands.append(hand)
        if overflow:
            n = 0
            while self.deck:
                hands[n].append(self.deal_card())
                n = (n + 1) % len(hands)
        return hands

    def deal_hands(self, num_players, num_cards):
        cards_to_deal = num_players * num_cards
        if cards_to_deal > len(self.deck):
            return self.deal_deck(num_players)
        hands = []
        for _ in range(num_players):
            hand = []
            for _ in range(num_cards):
                hand.append(self.deal_card())
            hands.append(hand)
        return hands
    
    def deal_card(self):
        return self.deck.pop()
    
class Pile:
    def __init__(self) -> None:
        self.stack = []
    
    def add(self, card):
        self.stack.append(card)

    def peek(self):
        if not self.stack:
            return None
        return self.stack[-1]
    
    def clear(self):
        self.stack = []

    def pop_all(self):
        return self.stack
    
class Hand:
    def __init__(self):
        self.cards = []

    def sort(self):
        self.cards.sort()

class Card:
    def __init__(self) -> None:
        self.face_up = True
        
    def flip_facedown(self):
        self.face_up = False

    def flip_faceup(self):
        self.face_up = True

    def is_faceup(self):
        return self.face_up
    