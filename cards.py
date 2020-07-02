import random
import constants

class Card():
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def show(self):
        print('{} of {}'.format(self.value, self.suit))

class Deck():

    def __init__(self):
        self.deck = self.create_new_deck()

    def create_new_deck(self): 
        # create and shuffle 52-card deck, used at init
        deck = []
        for suit in constants.SUITS:
            for value in range(1, 14):
                deck.append(Card(value, suit))
        random.shuffle(deck)
        
        return deck

    def get_top_card(self):
        self.deck[0].print_card()
        return self.deck[0]

    def show(self):
        for c in self.deck:
            c.print_card()


class Hand():

    def __init__(self, deck):
        self.deck = deck
        self.hand = self.create_hand()

    def create_hand(self):
        hand = []
        for i in range(0, constants.HAND_SIZE):
            hand.append(self.deck[i])
        for card in hand:
            self.deck.remove(card)

        return hand

    def add_card_type(self, card):
        self.hand.append(card)
    
    def add_card_attr(self, value, suit):
        self.hand.append(Card(value, suit))
    
    def show(self):
        for card in self.hand:
            card.print_card()
