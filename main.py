from cards import Deck, Card
from game import Game

main_deck = Deck()
deck = main_deck.deck

game = Game(deck)
game.get_player_names()

players = list(game.players)

# --- turn sequence ---

while True:
    player = players[0]
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

    # print matches
    print(f'{player.name}, you have {player.count_matches()} match(es)')


