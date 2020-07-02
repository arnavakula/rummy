from player import Player
from cards import Deck, Card

main_deck = Deck()
p1 = Player(main_deck.deck, 'Player 1')

p1.print_hand()
p1.count_matches()



   

