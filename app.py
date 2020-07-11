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
p1 = Player(deck)
p2 = Player(deck)
players = (p1, p2)
deck.discard_pile.append(deck.deck[0])
deck.deck.pop(0)

Builder.load_file('design.kv')

class GameScreen(Screen):
    has_clicked = False
    current_player = p1
    selected_card = None
    move_status = 0
        # 0 - draw (dark discard)
        # 1 - discard (dark draw)
        # 2 - wait (dark all)

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

        #TODO simplify this
        if hand[index].clicked and self.has_clicked: 
            button.background_normal = hand[index].get_image_name()
            hand[index].clicked = False
            self.has_clicked = False
            self.ids.title.text = f'Selected card: None'
            self.handle_card_disable()
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
            self.handle_card_disable()
        elif not hand[index].clicked and not self.has_clicked:
            button.background_normal = hand[index].get_pressed_image_name()
            hand[index].clicked = True
            self.has_clicked = True
            self.ids.title.text = f'Selected card: {hand[index].get_name()}'
            self.handle_card_disable()
        else:
            print('You should not have gotten here - unconditioned else')
    
    def handle_card_disable(self):
        if self.move_status == 0 and self.has_clicked:
            self.ids.draw.disabled = False
            self.ids.discard.disabled = True
        elif self.move_status == 1 and self.has_clicked:
            self.ids.draw.disabled = True
            self.ids.discard.disabled = False
        else:
            self.ids.draw.disabled = True
            self.ids.discard.disabled = True
        

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
        return deck.get_open_card()

    def display_open_card(self):
        return f"Open Card: {deck.get_open_card()}"
    
    def is_disabled(self, text):
        if ((text == 'Draw' and self.move_status == 1) or (text == 'Discard' and self.move_status == 0) or self.move_status == 2):
            return True
        else:
            return False

class DrawScreen(Screen):
    def draw_open_card(self):
        print('drawing open card')
    
    def display_open_card_image(self):
        return deck.discard_pile[-1].get_image_name()
    
    def draw_deck_card(self):
        print('drawing deck cards')

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__== '__main__':
    MainApp().run()   
