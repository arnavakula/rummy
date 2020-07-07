from cards import *
import math as m
import constants

class Player:

    def __init__(self, deck):
        self.deck = deck
        self.sorted = False
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
        return match_count
    
    def get_all_matches(self):
        matches = []
        for i in range(0, len(self.hand) - 2):
            for j in range(i + 1, len(self.hand) - 1):
                for k in range(j + 1, len(self.hand)):
                    if self.is_match((self.hand[i], self.hand[j], self.hand[k])):
                        matches.append((self.hand[i], self.hand[j], self.hand[k]))
        return matches

    # print for debugging
    def print_hand(self):
        print(f'\n{self.name}, this is your hand: ')
        for c in self.hand:
            c.show()
        print()
    
    def has_duplicates(self, matches):
        cards = []
        for match in matches:
            for card in match:
                cards.append(card)
        
        for card in cards:
            if cards.count(card) > 1:
                return True
        
        return False

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

    def won_game(self):
        matches = self.get_all_matches()
        for i in range(len(matches) - 2): #all but last two
            # print(i)
            for j in range(i + 1, len(matches) - 1):
                # print(j)
                for k in range(j + 1, len(matches)):
                    if not self.has_duplicates((matches[i], matches[j], matches[k])):
                        for c in matches[i]:
                            c.show()
                        print()
                        for c in matches[j]:
                            c.show()
                        print()
                        for c in matches[k]:
                            c.show()
                        return True
        
        return False       



# deck = Deck()
# p1 = Player(deck.deck)
# testing_hand = [Card(7, 'diamonds'), Card(8, 'diamonds'), Card(1, 'spades'), Card(2, 'spades'), Card(8, 'hearts'), Card(8, 'spades'), Card(3, 'spades'), Card(9, 'diamonds'), Card(8, 'clubs')]
# p1.hand = testing_hand
# print(p1.won_game())


    

