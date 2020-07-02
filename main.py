from player import Player
from cards import Deck, Card

main_deck = Deck().deck
p1 = Player(main_deck)

p1.print_hand()
p1.count_matches()