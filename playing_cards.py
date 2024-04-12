'''Contains classes for an indiviudal Playing Card and a deck of Playing Cards, as well as enums for RANKS and SUITS'''
import pygame
from enum import Enum
import os
import json
from cards import Card, Deck

class PlayingCard(Card):
    """A representation of a Playing Card with a rank and suit"""    
    def __init__(self, suit: "Suits", rank: "Ranks") -> None:
        super().__init__()
        self.suit = suit
        self.rank = rank
        
    def __init__(self, suit: "Suits", rank: "Ranks", image_path: str):
        """Creates an instance of a PlayingCard

        Args:
            suit (Suits(Enum)): the suit of the card (CLUBS, SPADES...)
            rank (Ranks(Enum)): the rank of the card (1-13)
            image_path (_type_): the path of the image for the card front
        """        
        super().__init__()
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(image_path)

    def equals(self, card: 'PlayingCard'):
        """Checks if the Ranks of this card is the same as the card compared against

        Args:
            card (PlayingCard): the card to compare with

        Returns:
            bool: True if the cards have the same rank, otherwise False
        """        
        return self.rank.value == card.rank.value
    
    def higher_than(self, card: 'PlayingCard', ace_high=True):
        """Compares this card with another and returns True if this one has a higher rank

        Args:
            card (PlayingCard): _description_
            ace_high (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """        
        if ace_high:
            if self.rank.value == 1 and card.rank.value != 1:
                return True
            elif card.rank.value == 1:
                return False
        return self.rank.value > card.rank.value

    def __str__(self):
        """returns a string representation of a card

        Returns:
            str: card rank + card suit
        """        
        return f"{str(self.rank.value)}{self.suit.name}"
    
    def __eq__(self, card: 'PlayingCard'):
        """Checks if two cards are exactly the same

        Args:
            card (PlayingCard): A playing card instance to compare with

        Returns:
            bool: True if both cards have the same suit and rank, otherwise false
        """        
        return self.rank == card.rank and self.suit == card.suit

    def __lt__(self, card: 'PlayingCard'):
        """Checks if this card is less than another card - suit first than rank, aces are high

        Args:
            card (PlayingCard): PlayingCard to compare with

        Returns:
            bool: True if this cards Suits value is less than the compared, or if the suits are the same,
                    True if this cards rank is less than the other
        """        
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
    """A Deck of PlayingCards"""    
    def __init__(self, jokers=False):
        """Creates a new deck of playing cards from playing_card_deck.json
            Generates a new deck if the file does not exist, or if it is unable to be read

        Args:
            jokers (bool, optional): If True the deck will be created with Jokers. Defaults to False.
        """        
        super().__init__()
        deck_obj = PlayingCardDeck._load_playing_card_deck()
        try:
            self._read_deck_json(deck_obj, jokers)
        except:
            deck_obj = self._create_playing_card_deck()
            self._save_playing_card_deck(deck_obj)
            self._read_deck_json(deck_obj, jokers)
    
    def _read_deck_json(self, deck_obj, jokers):
        # creates the deck of cards from the deck json object. Can error if the deck_obj is constructed badly      
        for suit in deck_obj["Suits"]:
            if suit == "JOKER":
                if jokers:
                    self.add_card(PlayingCard(Suits[suit], Ranks[suit], deck_obj["Suits"][suit]["0"]))
                    self.add_card(PlayingCard(Suits[suit], Ranks[suit], deck_obj["Suits"][suit]["1"]))
            else:
                for card_id in deck_obj["Suits"][suit]:
                    self.add_card(PlayingCard(Suits[suit], Ranks(int(card_id)), deck_obj["Suits"][suit][card_id]))
        self.card_back = pygame.image.load(deck_obj["Back"])

    def _save_playing_card_deck(deck_obj):
        # writes the deck_obj to playing_card_deck.json
        with open(os.path.join(os.getcwd(), 'playing_card_deck.json'), 'w') as file:
            json.dump(deck_obj, file, indent=4)

    def _create_playing_card_deck():
        # creates a json object representing a standard 52 card deck with two jokers
        deck = {}
        deck["Suits"] = {}
        for value in Ranks:
            if value == Ranks.JOKER:
                continue
            for suit in Suits:
                if suit == Suits.JOKER:
                    continue
                if suit.name not in deck["Suits"]:
                    deck["Suits"][suit.name] = {}
                if value.value > 1 and value.value < 10:
                    val = value.value
                else:
                    val = value.name[0]
                deck["Suits"][suit.name][str(value.value)] = f"images/{str(val)}{suit.name[0]}.png"
        deck["Suits"]["JOKER"] = {}
        for i in range(2):   
            deck["Suits"]["JOKER"][i] = f"images/{str(i + 1)}J.png"
        deck["Back"] = "images/1B.png"
        return deck

    def _load_existing_playing_card_deck(deck_file):
        # loads a json deck object from the given file
        with open(os.path.join(deck_file), 'r+') as file:
            deck_obj = json.load(file)
        return deck_obj

    def _load_playing_card_deck():
        # tries to load a json deck object from playing_card_deck.json
        # creates the file if it doesnt exist and then loads it
        try:
            deck_obj = PlayingCardDeck._load_existing_playing_card_deck('playing_card_deck.json')
        except:
            deck_obj = PlayingCardDeck._create_playing_card_deck()
            PlayingCardDeck._save_playing_card_deck(deck_obj)

        return deck_obj
    
class Suits(Enum):
    """
    Represents the standard playing card suits: CLUBS DIAMONDS SPADES HEARTS, and then JOKER for Jokers
    Suits are represented with integers in this order from 0-4
    """    
    CLUBS = 0
    DIAMONDS = 1
    SPADES = 2
    HEARTS = 3
    JOKER = 4

class Ranks(Enum):
    '''
    Represents the standard playing card ranks ACE-KING and then also JOKERS
    JOKERS are 0
    ACE-KING is 1-13
    '''
    JOKER = 0
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

if __name__ == "__main__":
    deck_obj = PlayingCardDeck._create_playing_card_deck()
    PlayingCardDeck._save_playing_card_deck(deck_obj)