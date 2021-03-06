import glob
import os
import time
from network import Network
import pickle
import threading

import cv2
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App

import consoleapp.game as game
from consoleapp.cards import *
from consoleapp.player import *

Builder.load_file('design.kv')

net = Network()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        self.deckobj = net.deckobj
        self.has_clicked = False
        self.selected_card = None
        self.highlighting_card = False
        self.current_player = net.player
        self.players = (net.players)
        self.t = threading.Thread(target=self.receive_data)
        self.t.setDaemon(True)
        self.t.start()
        super(Screen,self).__init__(**kwargs)

    def receive_data(self):
        while True:
            try:
                dobj, open_card, next_id = pickle.loads(net.client.recv(2048))
                with open('current_deckobj.dat', 'wb') as f:
                    f.truncate(0)
                    f.write(pickle.dumps(dobj))

                print('FOUND DATA FROM SERVER')
                if self.current_player.id == next_id:
                    self.current_player.move_status = 0

                self.reset_screen()
            except:
                pass

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

        for i in range(0, 9):
            cid = f'c{i + 1}'
            self.ids[cid].background_normal = hand[i].get_image_name()

        if self.current_player.move_status == 1 and len(self.get_current_hand()) > 9:
            self.ids.c10.disabled = False
            self.ids.c10.background_normal = hand[9].get_image_name()
        else:
            self.ids.c10.disabled = True
            self.ids.c10.background_normal = ''

        #reset chosen cards
        self.has_clicked = False
        for hand in (self.current_player.sorted_hand, self.current_player.hand):
            for card in hand:
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
        pass
        try:
            self.current_player = self.players[self.players.index(self.current_player) + 1]
        except IndexError:
            self.current_player = self.players[0]

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
        with open('current_deckobj.dat', 'rb') as f:
            dobj = pickle.loads(f.read())
            new_card = dobj.deck[0]

        self.current_player.add_card(new_card, dobj)
        self.current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

        with open('current_deckobj.dat', 'wb') as f:
            f.write(pickle.dumps(dobj))

    def draw_open_card(self):
        with open('current_deckobj.dat', 'rb') as f:
            dobj = pickle.loads(f.read())
            new_card = dobj.discard_pile[-1]

        self.current_player.add_card(new_card, dobj)
        self.current_player.move_status = 1
        self.reset_screen()
        self.highlight_card(new_card)

        with open('current_deckobj.dat', 'wb') as f:
            f.truncate(0)
            f.write(pickle.dumps(dobj))

    def highlight_card(self, new_card):
        cid = 'c10'
        if self.current_player.sorted:
            for c in self.current_player.sorted_hand:
                if c.value == new_card.value and c.suit == new_card.suit:
                    j = self.current_player.sorted_hand.index(c) + 1
                    cid = f'c{j}'

        self.ids[cid].background_normal = new_card.get_pressed_image_name()
        self.highlighting_card = True
        Clock.schedule_once(lambda dt: self.restore_image(cid, new_card), 1)

    def restore_image(self, cid, card):
        self.ids[cid].background_normal = card.get_image_name()
        self.highlighting_card = False

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
        with open('current_deckobj.dat', 'rb') as f:
            dobj = pickle.loads(f.read())

        self.current_player.discard(self.selected_card, dobj)
        self.current_player.move_status = 2
        next_id = 0
        try:
            next_id = self.players[self.current_player.id + 1].id
        except IndexError:
            pass

        self.deckobj.refresh_deck()
        net.send((dobj, self.selected_card, next_id))
        self.selected_card = None
        self.reset_screen()

    def display_open_card(self):
        with open('current_deckobj.dat', 'rb') as f:
            dobj = pickle.loads(f.read())

        try:
            self.ids.open_card_display.background_normal = dobj.discard_pile[-1].get_image_name()
            print('in display_open_card')
            dobj.discard_pile[-1].show()
            self.ids.open_card_display.disabled = False
            self.ids.open_card_display.text = ''
        except:
            self.ids.open_card_display.background_normal = ''
            self.ids.open_card_display.disabled = True
            self.ids.open_card_display.color =  (1, 1, 1, 1)
            self.ids.open_card_display.text = 'None (discard pile is empty)'

    def initialize_discard(self):
        return net.get_open_card().get_image_name()

    def click_open_card(self):
        pass

class PlayerWinScreen(Screen):
    def get_winning_message(self):
        global winning_player
        print(type(winning_player))
        return 'Congratulations, you won the game!'

    def exit_app(self):
        App.get_running_app().stop()

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

MainApp().run()
