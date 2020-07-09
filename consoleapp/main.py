from consoleapp.cards import Deck, Card
from consoleapp.game import Game

main_deck = Deck()
deck = main_deck.deck

game = Game(deck)
game.get_player_names()

players = list(game.players)
game_over = False

# --- turn sequence ---
while not game_over:
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

        game_over = player.won_game()
        if(game_over):
            print(f'{player.name}, you have won! Congratulations! Here is your winning hand:')
            player.print_hand()
            break

print('Game over')

