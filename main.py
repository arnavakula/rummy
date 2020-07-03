from cards import Deck, Card
from game import Game

main_deck = Deck()
deck = main_deck.deck

game = Game(deck)
game.get_player_names()

players = list(game.players)

game.discard(players[0])


# for player in game.players:
#     # show current player's hand
#     game.display_hand(player)

#     #display thrown card
#     print(f'')

#     # get turn 
#     turn = game.get_turn()

#     if turn == 0: # take deck card
#         pass
#     else: # take top card
#         pass

   

