from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from consoleapp.cards import *
from consoleapp.game import *
from consoleapp.player import *

deck = Deck()
player = Player(deck.deck)

Builder.load_file('design.kv')
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

class GameScreen(Screen):
    def get_card_fp(self, index):
        index = int(index[-1]) - 1
        return player.hand[index].get_image_name()

 
if __name__== '__main__':
    MainApp().run()   