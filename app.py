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
from consoleapp.game import *
from consoleapp.player import *

deck = Deck()
p1 = Player(deck)
current_player = p1
p2 = Player(deck)
players = (p1, p2)
deck.discard_pile.append(deck.deck[0])

deck.deck.pop(0)
p1.move_status = 0
p2.move_status = 2

Builder.load_file('design.kv')

class GameScreen(Screen):
    has_clicked = False
    selected_card = None
    highlighting_card = False
    global current_player
        # 0 - draw 
        # 1 - discard 
        # 2 - wait 

    def get_card_fp(self, button):
        button.font_size = '0sp'
        self.ids.open_card_display.background_color = (0, 0, 0, 1)
        if len(button.text) == 2:
            index = int(button.text[-1]) - 1
            p1.hand[index].show()
            return p1.hand[index].get_image_name()
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

        if current_player.move_status == 1 and len(self.get_current_hand()) > 9:
            self.ids.c10.disabled = False
            self.ids.c10.background_normal = hand[9].get_image_name()   
        else:
            self.ids.c10.disabled = True
            self.ids.c10.background_normal = ''

        #reset chosen cards
        self.has_clicked = False
        for card in current_player.hand:
            card.clicked = False
        
        for card in current_player.sorted_hand:
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
        global current_player
        if current_player == p1:
            current_player = p2
            self.ids.title.text = 'Player 2'
        else:
            current_player = p1
            self.ids.title.text = 'Player 1'

        self.ids.sort.text = 'Unsort' if current_player.sorted else 'Sort'
        
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
        if current_player.move_status == 0 and not self.has_clicked:
            self.ids.draw_open_card.disabled = False
            self.ids.draw_deck_card.disabled = False
            self.ids.discard.disabled = True
        elif current_player.move_status == 1 and self.has_clicked:
            self.ids.draw_open_card.disabled = True
            self.ids.draw_deck_card.disabled = True
            self.ids.discard.disabled = False
        else:
            self.ids.draw_open_card.disabled = True
            self.ids.draw_deck_card.disabled = True
            self.ids.discard.disabled = True

    def sort_hand(self):
        if current_player.sorted: #already sorted
            current_player.sorted = False
            self.ids.sort.text = 'Sort'
        else:
            current_player.sorted = True
            self.ids.sort.text = 'Unsort'

        self.reset_screen()
        self.ids.title.text = f'Selected card: None'

    def draw_deck_card(self):
        print(len(deck.deck))
        new_card = deck.deck[0]
        current_player.add_card(new_card, deck.deck)
        print(len(deck.deck))
        current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

    def draw_open_card(self):
        new_card = deck.discard_pile[-1]
        current_player.add_card(new_card, deck.discard_pile)
        current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

    def highlight_card(self, new_card):
        cid = 0
        try:
            if current_player.sorted: 
                for i in range(0, 9):
                    if current_player.sorted_hand[i].value == new_card.value and current_player.sorted_hand[i].suit == new_card.suit:
                        cid = 'c' + str(i + 1)
                        print(cid)
                        break
            else:
                cid = 'c10'
        except: 
            cid = 'c10'

        print('cid:{}'.format(cid))

        self.ids[cid].background_normal = new_card.get_pressed_image_name()
        self.highlighting_card = True
        Clock.schedule_once(lambda dt: self.restore_image(cid, new_card), 2)
    
    def restore_image(self, cid, card):
        self.ids[cid].background_normal = card.get_image_name()
        self.highlighting_card = False

    def get_open_card(self):
        return deck.get_open_card()

    def display_open_card(self):
        return f"Open Card: {deck.get_open_card()}"
    
    def get_init_disable(self, text):
        if current_player.move_status == 0 and text == 'Draw':
            return False
        else:
            return True
    
    def reset_screen(self):
        self.display_hand()
        for card in current_player.hand:
            card.clicked = False
        self.has_clicked = False

        self.handle_card_disable()
        self.display_open_card()

    def get_current_hand(self):
        return current_player.sorted_hand if current_player.sorted else current_player.hand

    def discard(self):
        current_player.discard(self.selected_card)
        self.selected_card = None
        current_player.print_hand()
        current_player.move_status = 0
        self.reset_screen()
    
    def display_open_card(self):
        try:
            self.ids.open_card_display.background_normal = deck.discard_pile[-1].get_image_name()
        except:
            self.ids.open_card_display.background_normal = ''
            self.ids.open_card_display.text = 'none'
            print(dir(self.ids.open_card_display))
            print('NO OPEN CARD')
        
    def click_open_card(self):
        pass
class DrawScreen(Screen):
    def draw_open_card(self):
        self.ids.draw_open_card.background_normal = deck.discard_pile[-1].get_image_name()
        deck.discard_pile.pop(-1)
        self.manager.transition.direction = 'right'
        self.manager.current = 'game_screen'

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
