from cards import Deck, Card
from game import Game

main_deck = Deck()
deck = main_deck.deck

game = Game(deck)
game.get_player_names()

players = list(game.players)

# -- turn sequence --

for player in players:
    print()
    # show hand
    player.print_hand()

    # sort deck (optional)
    game.user_sort(player)

    # show top card
    game.display_top_card()

    # get user move
    move = game.get_move()

    # handle turn
    game.handle_turn(player, move)

    # handle discard
    game.discard(player)
    print('NEW HAND')
    game.show(player.hand)
    print('NEW DISCARD PILE')
    game.show(game.discard_pile)

    break