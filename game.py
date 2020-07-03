from cards import Card, Deck
from player import Player

class UnsupportedValue(Exception):
    pass  

class Game():

    def __init__(self, deck):
        #TODO move deck init to here?
        self.wants_sorted = False
        self.deck = deck
        self.discard_pile = []
        self.initialize_discard_pile()
        self.players = self.create_players()

    def create_players(self):
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

    def initialize_discard_pile(self):
        self.discard_pile.append(self.deck[0])
        self.deck.pop(0)

    def user_sort(self, player):
        while True:
            try:
                move = input('Would you like to sort your hand[y/n]? ')
                if move.lower() != 'y' and move.lower() != 'n':
                    raise UnsupportedValue()
            except UnsupportedValue:
                print('You must enter y or n.')
            else:
                if move.lower() == 'y':
                    self.wants_sorted = True
                    player.sort_cards()
                    player.print_hand()
                break
            
    def get_move(self):
        possible_moves = {0: 'Select a card from the deck', 1: 'Select open card'}

        print('Enter the digit of the move you would like to make:')
        for move in possible_moves.keys():
            print(f'{move}: {possible_moves[move]}')

        while True:
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

    def handle_turn(self, player, move):
        if move == 0:
            new_card = self.deck[0]
            player.hand.append(new_card)
            self.deck.pop(0)
            print(f'\n {player.name}, you got the {new_card.get_name()} from the deck. \n')
        elif move == 1:
            self.discard_pile[-1].show()
            player.hand.append(self.discard_pile[-1])
            self.discard_pile.pop(-1)

        if self.wants_sorted:
            player.sort_cards()
        else:
            self.user_sort(player)

    def discard(self, player):
        while True:
            try:
                print(f'{player.name}, enter the digit in front of the card you wish to discard: ')
                for i in range(len(player.hand)):
                    print(f'{i + 1}: {player.hand[i].get_name()}')
                move = int(input())
            except ValueError:
                print('Sorry, you must enter an integer.')
            except IndexError:
                print('Sorry, that number does not correspond to one of the cards.')
            else:
                self.discard_pile.append(player.hand[move - 1])
                print(f'\n You discarded the {player.hand[move - 1].get_name()}. \n')
                player.hand.pop(move - 1)
                break

    def display_top_card(self):
        print(f'Open card: {self.discard_pile[-1].get_name()}.')

    # testing functions
    def show(self, cards):
        for card in cards:
            card.show()
    

# static_deck = Deck()
# p1, p2 = Player(static_deck.deck), Player(static_deck.deck)

# p1.print_hand()
# print('new player')
# p2.print_hand()

# print(len(static_deck.deck))
