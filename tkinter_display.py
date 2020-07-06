from tkinter import *
from player import Player
from cards import *

deck = Deck()
p1 = Player(deck.deck)
database = p1.hand


class Window:
    
    def __init__(self, window):
        self.window = window

        self.window.wm_title('Bookstore')

        #labels
        self.value = Label(self.window, text = 'Value')
        self.value.grid(row = 0, column = 0)

        self.suit = Label(self.window, text = 'Suit')
        self.suit.grid(row = 1, column = 0)

        self.open_card = Label(self.window, text = 'Open card: {}'.format(deck.deck[17].get_name()))
        self.open_card.grid(row = 2, column = 1)

        #entries
        self.value_var = StringVar()
        self.value_entry= Entry(self.window, textvariable = self.value_var)
        self.value_entry.grid(row = 0, column = 1)

        self.suit_var = StringVar()
        self.suit_entry = Entry(self.window, textvariable = self.suit_var)
        self.suit_entry.grid(row = 1, column = 1)

        #buttons
        view = Button(self.window, text = 'View All', width = 12, command = self.view_command)
        view.grid(row = 3, column = 3)

        discard = Button(self.window, text = 'Discard', width = 12, command = self.discard_command)
        discard.grid(row = 4, column = 3)
        
        draw = Button(self.window, text = 'Draw', width = 12, command = self.draw_command)
        draw.grid(row = 5, column = 3)

        #listbox, scrollbar
        self.lb = Listbox(self.window, height = 6, width = 36)
        self.lb.grid(row = 3, column = 0, rowspan = 6, columnspan = 2)

        self.sb = Scrollbar(self.window)
        self.sb.grid(row = 3, column = 2, rowspan = 6)

        self.lb.configure(yscrollcommand = self.sb.set)
        self.sb.configure(command = self.lb.yview)

        self.lb.bind('<<ListboxSelect>>', self.get_selected_row)

    #functions
    def refresh(self):
        self.lb.delete(0, END)
        self.view_command()

    def get_selected_row(self, event): 
        index = self.lb.curselection()[0]
        self.selected = self.lb.get(index)
        self.value_entry.delete(0, END)
        self.suit_entry.delete(0, END)
        self.value_entry.insert(END, self.selected.split(' ')[0])
        self.suit_entry.insert(END, self.selected.split(' ')[2])

    def view_command(self):
        self.lb.delete(0, END)
        for row in database:
            self.lb.insert(END, row.get_name())

    def discard_command(self):
        print('Discarding')

    def draw_command(self):
        print('Drawing')

#instantiate and initialize window
window = Tk()
Window(window)

#run window
window.mainloop()