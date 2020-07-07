from cards import Deck, Card
from game import Game

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

        # player.hand = [Card(7, 'diamonds'), Card(8, 'diamonds'), Card(1, 'spades'), Card(2, 'spades'), Card(8, 'hearts'), Card(8, 'spades'), Card(3, 'spades'), Card(9, 'diamonds'), Card(8, 'clubs')]

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

        game_over = player.won_game()
        if(game_over):
            print(f'{player.name}, you have won! Congratulations!')
            break

print('game over')

