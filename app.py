from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from consoleapp.cards import *
from consoleapp.game import *
from consoleapp.player import *

deck = Deck()
current_player = 1
p1 = Player(deck)
p2 = Player(deck)
players = (p1, p2)

Builder.load_file('design.kv')
class RootWidget(ScreenManager):
    pass

class GameScreen(Screen):
    sort_status = 0
    # 0 - unsorted
    # 1 - sorted
    move_status = 0
    # 0 - draw
    # 1 - discard
    # 2 - wait
    current_player = p1
    def get_card_fp(self, index):
        try:
            index = int(index[-1]) - 1
            p1.hand[index].show()
            return p1.hand[index].get_image_name()
        except:
            print('Change the id so that the last character is the corresponding index')

    def display_hand(self, player, needs_sorting):
        if not needs_sorting:
            self.ids.c1.background_normal = player.hand[0].get_image_name()
            self.ids.c2.background_normal = player.hand[1].get_image_name()
            self.ids.c3.background_normal = player.hand[2].get_image_name()
            self.ids.c4.background_normal = player.hand[3].get_image_name()
            self.ids.c5.background_normal = player.hand[4].get_image_name()
            self.ids.c6.background_normal = player.hand[5].get_image_name()
            self.ids.c7.background_normal = player.hand[6].get_image_name()
            self.ids.c8.background_normal = player.hand[7].get_image_name()
            self.ids.c9.background_normal = player.hand[8].get_image_name()
        else:
            self.ids.c1.background_normal = player.sorted_hand[0].get_image_name()
            self.ids.c2.background_normal = player.sorted_hand[1].get_image_name()
            self.ids.c3.background_normal = player.sorted_hand[2].get_image_name()
            self.ids.c4.background_normal = player.sorted_hand[3].get_image_name()
            self.ids.c5.background_normal = player.sorted_hand[4].get_image_name()
            self.ids.c6.background_normal = player.sorted_hand[5].get_image_name()
            self.ids.c7.background_normal = player.sorted_hand[6].get_image_name()
            self.ids.c8.background_normal = player.sorted_hand[7].get_image_name()
            self.ids.c9.background_normal = player.sorted_hand[8].get_image_name()

    def switch_player(self):
        if self.current_player == p1:
            self.current_player = p2
            self.ids.title.text = 'Player 2'
        else:
            self.current_player = p1
            self.ids.title.text = 'Player 1'
        
        self.display_hand(self.current_player, False)
        
    def sort_hand(self):
        if self.sort_status == 0:
            self.sort_status = 1
            self.display_hand(self.current_player, True)
            self.ids.sort.text = 'Unsort'
        else:
            self.sort_status = 0
            self.display_hand(self.current_player, False)
            self.ids.sort.text = 'Sort'

    def get_open_card(self):
        return f"Open Card: {deck.get_top_card()}"

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__== '__main__':
    MainApp().run()   