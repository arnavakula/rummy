from cards import *

class Player():

    def __init__(self, hand):
        self.hand = hand

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

    def count_matches(self, hand):
        count = 0
        for i in range(0, len(hand) - 2):
            for j in range(i + 1, len(hand) - 1):
                for k in range(j + 1, len(hand)):
                    if self.is_match((hand[i], hand[j], hand[k])):
                        count += 1
                        hand[i].show()
                        hand[j].show()
                        hand[k].show()
        print(f'count: {count}')


deck = Deck()
hand = Hand(deck.deck)
p1 = Player(hand.hand)

p1.count_matches(hand.hand)
