from cards import *
import constants

class Player():

    def __init__(self, deck):
        self.deck = deck
        self.name = ''
        self.hand = self.get_new_hand()
    
    # hand functions
    def get_new_hand(self):
        hand = []
        for i in range(0, constants.HAND_SIZE):
            hand.append(self.deck[i])
        for card in hand:
            self.deck.remove(card)

        return hand

    def give_card_type(self, card):
        self.hand.append(card)
    
    def give_card_attr(self, value, suit):
        self.hand.append(Card(value, suit))
        
    # match checking
    def is_match(self, trio):
        c1, c2, c3 = trio
        if c1.value == c2.value and c2.value == c3.value:
            print('same numbers')
            return True
        elif self.are_consecutive(trio) and self.are_same_suit(trio):
            print('sequence')
            return True
        else:
            return False

    def have_same_value(self, trio):
        v1, v2, v3 = sorted([c.value for c in trio])

        return True if v1 == v2 and v2 == v3 else False
    
    def are_consecutive(self, trio):
        v1, v2, v3 = sorted([c.value for c in trio])

        return True if v1 + 1 == v2 and v2 + 1 == v3 else False
    
    def are_same_suit(self, trio):
        s1, s2, s3 = [c.suit for c in trio]

        return True if s1 == s2 and s2 == s3 else False

    def count_matches(self):
        comb_count = 0
        match_count = 0
        for i in range(0, len(self.hand) - 2):
            for j in range(i + 1, len(self.hand) - 1):
                for k in range(j + 1, len(self.hand)):
                    comb_count += 1
                    if self.is_match((self.hand[i], self.hand[j], self.hand[k])):
                        match_count += 1
                        self.hand[i].show()
                        self.hand[j].show()
                        self.hand[k].show()
        print(f'count: {match_count}')

    # print for debugging
    def print_hand(self):
        for c in self.hand:
            c.show()
    
    # sorting cards
    def sort_cards(self):
        #suit and number 
        #TODO implement multi-criteria checking
        new_hand = []
        value_sort = [[], [], [], []]

        for card in self.hand:
            value_sort[constants.SUITS.index(card.suit)].append(card.value)

        for suit in value_sort: 
            suit.sort()
            for value in suit: 
                new_hand.append(Card(value, constants.SUITS[value_sort.index(suit)]))
            
        self.hand = new_hand
        
        #problem - find what card in hand has a certain value
        


        



# deck = Deck()
# p1 = Player(deck.deck)

# p1.print_hand()
# print('------------------------')
# p1.sort_cards()

# p1.print_hand()

