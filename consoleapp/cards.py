import random
import consoleapp.constants as constants

class Card():
    
    def __init__(self, value, suit):
        self.value = value
        self.translated_value = self.get_translated_value()
        self.suit = suit
        self.clicked = False
    
    def get_image_name(self):
        suit = self.suit[0].upper()
        if self.value > 10 or self.value < 2:
            val = self.translated_value.upper()[0]
            fp = f'card_images//{val}{suit}.png'
        else:
            fp = f'card_images//{self.value}{suit}.png'
        return fp

    def get_pressed_image_name(self):
        suit = self.suit[0].upper()
        if self.value > 10 or self.value < 2:
            val = self.translated_value.upper()[0]
            fp = f'pressed_card_images//{val}{suit}.png'
        else:
            fp = f'pressed_card_images//{self.value}{suit}.png'
        return fp
    
    def get_translated_value(self):
        face_cards = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

        if self.value in face_cards.keys():
            return face_cards[self.value]
        else:
            return self.value

    def get_name(self):
        return (f'{self.translated_value} of {self.suit}')

    def show(self):
        print('{} of {}'.format(self.translated_value, self.suit))

class Deck():

    def __init__(self):
        self.deck = self.create_new_deck()
        self.discard_pile = []

    def create_new_deck(self): 
        # create and shuffle 52-card deck, used at init
        deck = []
        for suit in constants.SUITS:
            for value in range(1, 14):
                deck.append(Card(value, suit))
        random.shuffle(deck)
        
        return deck
    
    def get_top_card(self):
        try:
            return self.discard_pile[0].get_name()
        except:
            return 'no card'

    def show(self):
        for c in self.deck:
            c.print_card()