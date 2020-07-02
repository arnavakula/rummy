from player import Player
from cards import Deck, Card

main_deck = Deck()
p1 = Player(main_deck.deck, 'Player 1')

p1.print_hand()
p1.count_matches()

def get_turn():
    is_valid = False
    possible_moves = {0: 'Select a card from the deck', 1: 'Select thrown card'}

    print('Enter the digit of the move you would like to make')
    for move in possible_moves.keys():
        print(f'{move}: {possible_moves[move]}')

    while not is_valid:
        try:
            move = int(input())

            if move != 0 and move != 1:
                raise ValueError
        except ValueError:
            print('Sorry, that input was not one of the given options.\n')
            print('Enter the digit of the move you would like to make:')
            for move in possible_moves.keys():
                print(f'{move}: {possible_moves[move]}')
        else:
            return move

   

