import pygame
from enum import Enum
import os
import json
from cards import Card, Deck

class PlayingCard(Card):
    def __init__(self, suit, rank) -> None:
        super().__init__()
        self.suit = suit
        self.rank = rank
        if rank.value >= 2 and rank.value < 10:
            self.image = pygame.image.load(f"images/{str(self.rank.value)}{self.suit.name[0]}.png")
        else:
            self.image = pygame.image.load(f"images/{self.rank.name[0]}{self.suit.name[0]}.png")

    def __init__(self, suit, rank, image_path):
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(image_path)

    def equals(self, card):
        return self.rank.value == card.rank.value
    
    def higher_than(self, card, ace_high=True):
        if ace_high:
            if self.rank.value == 1 and card.rank.value != 1:
                return True
            elif card.rank.value == 1:
                return False
        return self.rank.value > card.rank.value

    def __str__(self):
        return f"{str(self.rank.value)}{self.suit.name}"
    
    def __eq__(self, card):
        return self.rank == card.rank and self.suit == card.suit

    def __lt__(self, card):
        if self.suit.value < card.suit.value:
            return True
        elif self.suit.value > card.suit.value:
            return False
        if self.rank.value == 1 and card.rank.value != 1:
            return False
        elif card.rank.value == 1 and self.rank.value != 1:
            return True
        return self.rank.value < card.rank.value
      

class PlayingCardDeck(Deck):
    def __init__(self, include_jokers) -> None:
        super().__init__()
        for value in Ranks:
            for suit in Suits:
                card = Card(suit, value)
                self.deck.append(card)

    def __init__(self):
        super().__init__()
        deck_obj = PlayingCardDeck.load_playing_card_deck()
        for suit in deck_obj["Suits"]:
            for card_id in deck_obj["Suits"][suit]:
                self.deck.append(PlayingCard(Suits[suit], Ranks(int(card_id)), deck_obj["Suits"][suit][card_id]))

    def save_playing_card_deck(deck_obj):
        with open(os.path.join(os.getcwd(), 'playing_card_deck.json'), 'w') as file:
            json.dump(deck_obj, file, indent=4)

    def create_playing_card_deck():
        deck = {}
        deck["Suits"] = {}
        for value in Ranks:
            for suit in Suits:
                if suit.name not in deck["Suits"]:
                    deck["Suits"][suit.name] = {}
                if value.value > 1 and value.value < 10:
                    val = value.value
                else:
                    val = value.name[0]
                deck["Suits"][suit.name][str(value.value)] = f"images/{str(val)}{suit.name[0]}.png"
        deck["Back"] = "images/1B.png"
        return deck

    def load_existing_playing_card_deck(deck_file):
        with open(os.path.join(deck_file), 'r+') as file:
            deck_obj = json.load(file)
        return deck_obj

    def load_playing_card_deck():
        try:
            deck_obj = PlayingCardDeck.load_existing_playing_card_deck('playing_card_deck.json')
        except:
            deck_obj = PlayingCardDeck.create_playing_card_deck()
            PlayingCardDeck.save_playing_card_deck(deck_obj)

        return deck_obj
    
class Suits(Enum):
    CLUBS = 0
    DIAMONDS = 1
    SPADES = 2
    HEARTS = 3

class Ranks(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13