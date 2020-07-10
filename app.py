import glob
import os

import cv2
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
    has_clicked = False
    current_player = p1

    def get_card_fp(self, index):
        try:
            index = int(index[-1]) - 1
            p1.hand[index].show()
            return p1.hand[index].get_image_name()
        except:
            print('Change the id so that the last character is the corresponding index')

    def display_hand(self):
        hand = self.current_player.sorted_hand if self.current_player.sorted else self.current_player.hand
       
        self.ids.c1.background_normal = hand[0].get_image_name()
        self.ids.c2.background_normal = hand[1].get_image_name()
        self.ids.c3.background_normal = hand[2].get_image_name()
        self.ids.c4.background_normal = hand[3].get_image_name()
        self.ids.c5.background_normal = hand[4].get_image_name()
        self.ids.c6.background_normal = hand[5].get_image_name()
        self.ids.c7.background_normal = hand[6].get_image_name()
        self.ids.c8.background_normal = hand[7].get_image_name()
        self.ids.c9.background_normal = hand[8].get_image_name()

        #reset chosen cards
        self.has_clicked = False
        for card in self.current_player.hand:
            card.clicked = False
        
        for card in self.current_player.sorted_hand:
            card.clicked = False

    def create_hls_deck(self):
        images = glob.glob('card_images//*.png')
        for fp in images: 
            img = cv2.imread(fp) 
            pressed_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
            base = os.path.splitext(fp)[0].split('/')[1]
            path = f'pressed_card_images//{base}.png'
            cv2.imwrite(path, pressed_img)

    def switch_player(self):
        if self.current_player == p1:
            self.current_player = p2
            self.ids.title.text = 'Player 2'
        else:
            self.current_player = p1
            self.ids.title.text = 'Player 1'

        self.ids.sort.text = 'Unsort' if self.current_player.sorted else 'Sort'
        self.display_hand()

    def handle_clicked_card(self, button):
        index = int(button.text[-1]) - 1
        hand = self.current_player.sorted_hand if self.current_player.sorted else self.current_player.hand

        if hand[index].clicked and self.has_clicked: 
            button.background_normal = hand[index].get_image_name()
            hand[index].clicked = False
            self.has_clicked = False
            self.ids.title.text = f'Selected card: None'
        elif hand[index].clicked and not self.has_clicked:
            print('You clicked a card and it did not register')
        elif not hand[index].clicked and self.has_clicked:
            self.display_hand()
            for card in hand:
                card.clicked = False
            button.background_normal = hand[index].get_pressed_image_name()
            self.has_clicked = True
            hand[index].clicked = True
            self.ids.title.text = f'Selected card: {hand[index].get_name()}'
        elif not hand[index].clicked and not self.has_clicked:
            button.background_normal = hand[index].get_pressed_image_name()
            hand[index].clicked = True
            self.has_clicked = True
            self.ids.title.text = f'Selected card: {hand[index].get_name()}'
        else:
            print('You should not have gotten here - unconditioned else')

    def sort_hand(self):
        if self.current_player.sorted: #already sorted
            self.current_player.sorted = False
            self.ids.sort.text = 'Sort'
        else:
            self.current_player.sorted = True
            self.ids.sort.text = 'Unsort'

        self.display_hand()
        self.ids.title.text = f'Selected card: None'

    def go_to_draw_screen(self):
        self.manager.current = 'draw_screen'
        
    def get_open_card(self):
        return f"Open Card: {deck.get_top_card()}"

class DrawScreen(Screen):
    def draw_open_card(self):
        print('drawing open card')
    
    def draw_deck_card(self):
        print('drawing deck cards')


class MainApp(App):
    def build(self):
        return RootWidget()

if __name__== '__main__':
    MainApp().run()   
