#!/usr/bin/env python
"""Treasure Chest GUI using Tkinter."""

from __future__ import print_function

from functools import partial
from Tkinter import *
import tkSimpleDialog

from ..model import Board, EMPTY, InputError, MIN_SIZE, MAX_SIZE
from ..model import X as PLAYER_X, Y as PLAYER_Y  # X and Y conflict with Tkinter
from .messages import MESSAGES
from .resources import ResourceManager
from .tk_aboutbox import AboutBox

APP_NAME = 'Treasure Chest'
DESCRIPTION = 'A simple board game'
COPYRIGHT = u'''Copyright \xA9 2012 Chris Wong
Images from the Nautical Icon Set by ~manda-pie'''
WEBSITE = 'https://github.com/lfairy/treasure-chest'

DEFAULT = 0
SELECTED = 1
PULSING = 2

def main():
    root = Tk()
    app = Application(root)
    app.mainloop()

class Application(Frame):
    def __init__(self, master):
        master.title(APP_NAME)
        Frame.__init__(self, master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.menu = Menu(self.master)

        self.game_menu = Menu(self.menu, tearoff=False)
        self.game_menu.add_command(label='New', command=self.new)
        self.game_menu.add_command(label='Preferences', command=self.preferences)
        self.game_menu.add_separator()
        self.game_menu.add_command(label='About', command=self.about)
        self.game_menu.add_separator()
        self.game_menu.add_command(label='Quit', command=self.master.quit)
        self.menu.add_cascade(label='Game', menu=self.game_menu)

        self.master['menu'] = self.menu

        var = StringVar()
        self.status = Label(self, textvariable=var, font='Verdana 16')
        self.status.pack(fill=X, pady=5)

        self.board = TkBoard(self, var.set)
        self.board_size = 5
        self.new()

    def new(self):
        self.board.restart(self.board_size)
        self.board.pack(padx=16, pady=16)

    def preferences(self):
        prefs = Preferences(self.master, self.board_size)
        try:
            self.master.wait_window(prefs)
        except TclError:  # "Bad window path name"
            pass

        new_size = prefs.result
        if new_size is not None:
            self.board_size = new_size
            self.new()

    def about(self):
        about = AboutBox(self.master, APP_NAME, DESCRIPTION, COPYRIGHT, WEBSITE)
        try:
            self.master.wait_window(about)
        except TclError:  # "Bad window path name"
            pass

class TkBoard(Frame):
    def __init__(self, master, set_status):
        Frame.__init__(self, master)
        self.resources = ResourceManager()
        self.set_status = set_status
        self.set_status('hello')

    def restart(self, size):
        """Restart the Treasure Chest game."""

        self.controller = Controller(self, size)

        # Recreate all the buttons in the grid
        self.destroy_children()
        self.squares = []
        for y in range(size):
            row = []
            for x in range(size):
                row.append(Square(self, x, y))
            self.squares.append(row)

        self.update_view()

    def destroy_children(self):
        """Destroy all the buttons in the grid."""
        if hasattr(self, 'squares'):
            for row in self.squares:
                for child in row:
                    child.destroy()
            del self.squares

    def update_view(self):
        """Update the button labels to reflect the inner state."""
        for brow, srow in zip(self.controller.board, self.squares):
            for piece, square in zip(brow, srow):
                square.piece = piece
                square.placate()

    def handle_click(self, button):
        self.controller.handle_click(button)

    def finish(self):
        """The game has finished: disable all the buttons."""
        for row in self.squares:
            for child in row:
                child['state'] = DISABLED

class Controller:
    def __init__(self, view, size):
        self.board = Board(size)
        self.view = view
        self.player = PLAYER_X

        self.handler, message = self.start_move_()
        self.view.set_status(message)

    def handle_click(self, button):
        self.handler, message = self.handler(button)
        if message is not None:
            self.view.set_status(message)

    def start_move(self, button):
        # Get all the valid moves starting from where the user clicked
        self.start = (button.x, button.y)
        self.valid_ends = self.board.valid_moves_from(self.player, self.start)

        # Highlight all the positions the piece can move to
        for (x, y) in self.valid_ends:
            self.view.squares[y][x].excite(PULSING)

        # Only try to finish the move if there are actual valid moves
        if self.valid_ends:
            button.excite(SELECTED)
            return self.finish_move_()
        else:
            return self.start_move_()

    start_move_ = lambda self: (self.start_move, MESSAGES['prompt_move'](self.player))

    def finish_move(self, button):
        end = (button.x, button.y)
        if end in self.valid_ends:
            # Make the move
            winner = self.board.move(self.player, self.start, end)
            self.next_player()
            self.view.update_view()
            if winner is None:
                # Give control to the next player
                return self.start_move_()
            else:
                # Finish him!
                self.view.finish()
                return self.end_game_(winner)
        else:
            # Prompt for another move
            self.view.update_view()
            return self.start_move_()

    finish_move_ = lambda self: (self.finish_move, None)

    def end_game(self, winner, *ignored):
        return self.end_game_(winner)

    end_game_ = lambda self, winner: (partial(self.end_game, winner),
                                      MESSAGES['win'](winner))

    def next_player(self):
        if self.player == PLAYER_X:
            self.player = PLAYER_Y
        else:
            self.player = PLAYER_X

class Square(Button, object):
    def __init__(self, master, x, y):
        Button.__init__(self, master, width=56, height=56, border=0,
                command=self.click)
        self.grid(row=y, column=x)
        self.x = x
        self.y = y

        # Reset the button state
        self.piece = EMPTY
        self.placate()

    def get_piece(self):
        return self._piece

    def set_piece(self, new):
        self._piece = new
        self['image'] = self.master.resources.load(new)

    piece = property(get_piece, set_piece)

    def click(self):
        self.master.handle_click(self)

    def placate(self):
        self.excite(DEFAULT)

    def excite(self, mode):
        self['background'], self['activebackground'] = {
                DEFAULT: ('#eeeeee', '#ffffff'),
                SELECTED: ('#99aaff', '#aaccff'),
                PULSING: ('#66cc66', '#99ee99'),
                }[mode]

class Preferences(tkSimpleDialog.Dialog):
    def __init__(self, master, board_size):
        self._init_board_size = board_size
        tkSimpleDialog.Dialog.__init__(self, master)

    def body(self, master):
        group = LabelFrame(master, text=MESSAGES['board_size'], padx=5, pady=5)
        group.pack(padx=10, pady=10)

        self.v = IntVar()
        for value in range(MIN_SIZE, MAX_SIZE+1, 2):
            b = Radiobutton(group, text=str(value), variable=self.v, value=value)
            b.pack(anchor=W)
            if value == self._init_board_size:
                b.select()

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="OK", width=8, command=self.ok, default=ACTIVE)
        w.pack(side=RIGHT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=8, command=self.cancel)
        w.pack(side=RIGHT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side=RIGHT)

    def apply(self):
        self.result = self.v.get()

if __name__ == '__main__':
    main()
