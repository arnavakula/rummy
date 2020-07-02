import random
import constants

class Card():
    
    def __init__(self, value, suit):
        self.value = value
        self.translated_value = self.get_translated_value()
        self.suit = suit
    
    def get_translated_value(self):
        face_cards = {11: 'Jack', 12: 'Queen', 13: 'King'}

        if self.value > 10:
            return face_cards[self.value]
        else:
            return self.value

        
    def show(self):
        print('{} of {}'.format(self.translated_value, self.suit))

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