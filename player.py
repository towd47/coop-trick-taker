class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.hand = []
        self.goals = []
        self.communicated = False
        self.communicated_card = None

    def is_captain(self):
        for card in self.hand:
            if card.is_captain_card():
                return True
        return False
    
    def set_hand(self, hand):
        self.hand = hand

    def take_goal(self, goal):
        self.goals.append(goal)
    
    # def is_valid_play(self, card, suit_to_follow):
    #     if card not in self.hand:
    #         return False        
    #     if suit_to_follow and card.suit != suit_to_follow and self.has_suit(suit_to_follow):
    #         return False
    #     return True
    
    # def has_suits(self):
    #     return set([card.suit for card in self.hand])
    
    def has_suit(self, suit):
        for card in self.hand:
            if card.suit == suit:
                return True
        return False
    
    def play_card(self, card):
        self.hand.remove(card)
        if self.communicated and card == self.communicated_card:
            self.communicated_card = None