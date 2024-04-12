'''Cards contains basic implementations for a Deck, Card, and Pile'''
import random

class Deck:
    '''Deck provides basic deck implementation for shuffling and dealing cards'''
    def __init__(self) -> None:
        self._deck = []
        self.card_back = None
    
    def shuffle(self):
        '''Randomizes the order of the card list'''
        random.shuffle(self._deck)

    def deal_deck(self, num_players, overflow = False):
        '''Deals the deck into number of hands equal to num_players
        
        Args:
            num_players (int): the number of hands that the deck should be divided into
            overflow (bool): Deals the whole deck if True, deals an even number of cards to every player and leaves extra in the deck if False (default is False)
        
        Returns:
            list: a list of lists of cards representing the dealt hands    
        '''

        num_cards = int(len(self._deck) / num_players)
        hands = []
        for _ in range(num_players):
            hand = []
            for _ in range(num_cards):
                hand.append(self.deal_card())
            hands.append(hand)
        if overflow:
            n = 0
            while self._deck:
                hands[n].append(self.deal_card())
                n = (n + 1) % len(hands)
        return hands

    def deal_hands(self, num_players, num_cards):
        '''Deals the deck into number of hands equal to num_players, each containing num_cards cards
        
        Args:
            num_players (int): The number of hands that the deck should be divided into
            num_cards: The number of cards each player should be dealt. If this exceeds the number of remaining cards in
                the deck, each player will be dealt the same amount of cards using as much of the deck as possible
        
        Returns:
            list: a list of lists of cards representing the dealt hands    
        '''
        cards_to_deal = num_players * num_cards
        if cards_to_deal > len(self._deck):
            return self.deal_deck(num_players)
        hands = []
        for _ in range(num_players):
            hand = []
            for _ in range(num_cards):
                hand.append(self.deal_card())
            hands.append(hand)
        return hands
    
    def deal_card(self):
        '''returns the top card of the deck'''
        return self._deck.pop()
    
    def add_card(self, card, top=False):
        '''adds a card to the bottom of the deck, or the top if top = True'''
        if top:
            self._deck.append(card)
        else:
            self._deck.insert(0, card)

    def add_cards(self, cards, top=False):
        '''adds a list of cards to the bottom of the deck, or the top if top = True'''
        if top:
            self._deck.extend(cards)
        else:
            self._deck = cards.extend(self._deck)
            
    def clear(self):
        '''clears all cards in the deck by setting self.cards to an empty list'''
        self._deck = []
    
class Pile:
    '''A basic representation of a pile of cards'''
    def __init__(self) -> None:
        self.stack = []
    
    def add(self, card):
        '''adds a card to the top of the pile'''
        self.stack.append(card)

    def peek(self):
        '''returns the top card of the pile if there are cards in the pile, otherwise returns none'''
        if not self.stack:
            return None
        return self.stack[-1]
    
    def clear(self):
        '''empties the pile by setting the stack to an empty list'''
        self.stack = []

    def get_all(self):
        '''returns a list of all cards in the pile'''
        return self.stack
    
class Hand:
    def __init__(self):
        self.cards = []

    def sort(self):
        self.cards.sort()

class Card:
    '''A basic representation of a card that can be flipped up or down'''
    def __init__(self) -> None:
        self.face_up = True
        self.image = None
        
    def flip_facedown(self):
        '''sets the card's faceup property to False'''
        self.face_up = False

    def flip_faceup(self):
        '''sets the card's faceup property to True'''
        self.face_up = True

    def is_faceup(self):
        '''returns whether or not the card is faceup'''
        return self.face_up
    