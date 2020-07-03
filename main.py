from cards import Deck, Card
from game import Game

main_deck = Deck()
deck = main_deck.deck

game = Game(deck)
game.get_player_names()

players = list(game.players)

# -- turn sequence --


# show hand
players[0].print_hand()

# show top card
game.display_top_card()

# get user move
move = game.get_move()

# handle deck card
if move == 0:
    game.handle_turn(players[0], move)
    print('NEW HAND BELOW')
    players[0].print_hand()
    



    # handle open card

    # discard 



