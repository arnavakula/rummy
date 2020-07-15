import glob
import os
import time
from kivy.clock import Clock

import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager

from consoleapp.cards import *
import consoleapp.game as game
from consoleapp.player import *

Builder.load_file('design.kv')

class PlayerSelectScreen(Screen):
    pass

class GameScreen(Screen):
    deckobj = Deck()
    p1, p2 = Player(deckobj), Player(deckobj)
    has_clicked = False
    selected_card = None
    highlighting_card = False
    current_player = p1
    p1.move_status = 0
    p2.move_status = 2
    players = (p1, p2)

    def get_card_fp(self, button):
        button.font_size = '0sp'
        if len(button.text) == 2:
            index = int(button.text[-1]) - 1
            self.current_player.hand[index].show()
            return self.current_player.hand[index].get_image_name()
        else: 
            button.disabled = True
            return ''

    def display_hand(self):
        hand = self.get_current_hand()
        self.ids.c1.id = 'c1'
       
        self.ids.c1.background_normal = hand[0].get_image_name()
        self.ids.c2.background_normal = hand[1].get_image_name()
        self.ids.c3.background_normal = hand[2].get_image_name()
        self.ids.c4.background_normal = hand[3].get_image_name()
        self.ids.c5.background_normal = hand[4].get_image_name()
        self.ids.c6.background_normal = hand[5].get_image_name()
        self.ids.c7.background_normal = hand[6].get_image_name()
        self.ids.c8.background_normal = hand[7].get_image_name()
        self.ids.c9.background_normal = hand[8].get_image_name()

        if self.current_player.move_status == 1 and len(self.get_current_hand()) > 9:
            self.ids.c10.disabled = False
            self.ids.c10.background_normal = hand[9].get_image_name()   
        else:
            self.ids.c10.disabled = True
            self.ids.c10.background_normal = ''

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
        if self.current_player == self.p1:
            self.current_player = self.p2
            self.ids.title.text = 'Player 2'
        else:
            self.current_player = self.p1
            self.ids.title.text = 'Player 1'

        self.ids.sort.text = 'Unsort' if self.current_player.sorted else 'Sort'
        
        self.reset_screen()

    def handle_clicked_card(self, button):
        if not self.highlighting_card:
            index = int(button.text[-1]) - 1
            hand = self.get_current_hand()

            if hand[index].clicked and self.has_clicked: 
                button.background_normal = hand[index].get_image_name()
                self.reset_screen()
                self.ids.title.text = f'Selected card: None'
            elif hand[index].clicked and not self.has_clicked:
                print('You clicked a card and it did not register')
            else:
                if not hand[index].clicked and self.has_clicked:
                    self.reset_screen()
                button.background_normal = hand[index].get_pressed_image_name()
                hand[index].clicked = True
                self.has_clicked = True
                self.ids.title.text = f'Selected card: {hand[index].get_name()}'
                self.handle_card_disable()
                self.selected_card = hand[index]

    def handle_card_disable(self):
        if self.current_player.move_status == 0 and not self.has_clicked:
            self.ids.draw_open_card.disabled = False
            self.ids.draw_deck_card.disabled = False
            self.ids.discard.disabled = True
        elif self.current_player.move_status == 1 and self.has_clicked:
            self.ids.draw_open_card.disabled = True
            self.ids.draw_deck_card.disabled = True
            self.ids.discard.disabled = False
        else:
            self.ids.draw_open_card.disabled = True
            self.ids.draw_deck_card.disabled = True
            self.ids.discard.disabled = True

    def sort_hand(self):
        if self.current_player.sorted: #already sorted
            self.current_player.sorted = False
            self.ids.sort.text = 'Sort'
        else:
            self.current_player.sorted = True
            self.ids.sort.text = 'Unsort'

        self.reset_screen()
        self.ids.title.text = f'Selected card: None'

    def draw_deck_card(self):
        new_card = self.deckobj.deck[0]
        self.current_player.add_card(new_card, self.deckobj.deck)
        self.current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

    def draw_open_card(self):
        new_card = self.deckobj.discard_pile[-1]
        self.current_player.add_card(new_card, self.deckobj.discard_pile)
        self.current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

    def highlight_card(self, new_card):
        cid = 'c10'
        if self.current_player.sorted:
            for c in self.current_player.sorted_hand:
                if c.value == new_card.value and c.suit == new_card.suit:
                    j = self.current_player.sorted_hand.index(c) + 1
                    cid = f'c{j}'

        self.ids[cid].background_normal = new_card.get_pressed_image_name()
        self.highlighting_card = True
        Clock.schedule_once(lambda dt: self.restore_image(cid, new_card), 2)
    
    def restore_image(self, cid, card):
        self.ids[cid].background_normal = card.get_image_name()
        self.highlighting_card = False

    def get_open_card(self):
        return self.deckobj.get_open_card()

    def display_open_card(self):
        return f"Open Card: {self.deckobj.get_open_card()}"
    
    def get_init_disable(self, text):
        if self.current_player.move_status == 0 and text == 'Draw':
            return False
        else:
            return True
    
    def reset_screen(self):
        self.display_hand()
        for card in self.current_player.hand:
            card.clicked = False
        self.has_clicked = False

        self.handle_card_disable()
        self.display_open_card()

    def get_current_hand(self):
        return self.current_player.sorted_hand if self.current_player.sorted else self.current_player.hand

    def discard(self):
        self.current_player.discard(self.selected_card)
        self.selected_card = None
        self.current_player.move_status = 2
        print('Has the player won: {}'.format(self.current_player.won_game()))
        try:
            self.players[self.players.index(self.current_player) + 1].move_status = 0
        except IndexError:
            self.players[0].move_status = 0
        finally:
            self.reset_screen()
    
    def display_open_card(self):
        try:
            self.ids.open_card_display.background_normal = self.deckobj.discard_pile[-1].get_image_name()
            self.ids.open_card_display.disabled = False
            self.ids.open_card_display.text = ''
        except:
            self.ids.open_card_display.background_normal = ''
            self.ids.open_card_display.disabled = True
            self.ids.open_card_display.color =  (1, 1, 1, 1)
            self.ids.open_card_display.text = 'None (discard pile is empty)'

    def initialize_discard(self):
        self.deckobj.discard_pile.append(self.deckobj.deck[0])
        self.deckobj.deck.pop(0)
        return self.deckobj.discard_pile[-1].get_image_name()

    def click_open_card(self):
        pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__== '__main__':
    MainApp().run()   
