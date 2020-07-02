from player import Player
from cards import Card, Deck

class UnsupportedValue(Exception):
    pass
class Game():

    def __init__(self, deck):
        self.deck = deck
        self.players = self.get_players()

    def get_players(self):
        is_valid = False
        players = []
        
        while not is_valid:
            try:
                num = int(input('Enter the number of players playing: '))
                # TODO allow for more than two players with multiple decks
                if num != 2:
                    raise UnsupportedValue()
            except ValueError:
                print('Sorry, you must enter a number.')
            except UnsupportedValue:
                print('Sorry, you cannot play with that many players.')
            else:
                break
        
        for i in range(num):
            players.append(Player(self.deck))

        return players
            


    
    def get_player_names(self):
        names = {}
        for i in range(len(self.players)):
            name = input(f'Player {i + 1}, enter your name: ')
            self.players[i].name = name

    def get_turn(self):
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
                for move in possible_moves.keys():
                    print(f'{move}: {possible_moves[move]}')
            else:
                return move

    def display_hand(self, player):
        player.print_hand()

# static_deck = Deck()
# p1, p2 = Player(static_deck.deck), Player(static_deck.deck)

# p1.print_hand()
# print('new player')
# p2.print_hand()

# print(len(static_deck.deck))


