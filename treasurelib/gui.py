#!/usr/bin/env python
"""Treasure Chest GUI using Tkinter."""

from __future__ import print_function

from Tkinter import *
import tkMessageBox

from model import Board, EMPTY, InputError, X, Y

COPYRIGHT = u'''
\xA9 2012 Chris Wong.

I like shorts, they are comfortable and easy to wear.
'''.strip()

DEFAULT = 0
SELECTED = 1
PULSING = 2

def main():
    root = Tk()
    app = Application(root)
    app.mainloop()

class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.menu = Menu(self.master)

        self.game_menu = Menu(self.menu, tearoff=False)
        self.game_menu.add_command(label='New', command=self.new)
        self.game_menu.add_command(label='Preferences', command=lambda: print('hello'))
        self.game_menu.add_separator()
        self.game_menu.add_command(label='About', command=self.about)
        self.game_menu.add_separator()
        self.game_menu.add_command(label='Quit', command=self.master.quit)
        self.menu.add_cascade(label='Game', menu=self.game_menu)

        self.master['menu'] = self.menu

        self.board = TkBoard(self)
        self.new()

    def new(self):
        self.board.restart(5)
        self.board.pack()

    def about(self):
        tkMessageBox.showinfo('Treasure Chest', COPYRIGHT)

class TkBoard(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

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

class Controller:
    def __init__(self, view, size):
        self.board = Board(size)
        self.view = view
        self.handle_click = self.start_move
        self.player = X

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
            self.handle_click = self.finish_move

    def finish_move(self, button):
        end = (button.x, button.y)
        if end in self.valid_ends:
            # Make the move
            winner = self.board.move(self.player, self.start, end)
            self.next_player()
            self.view.update_view()
            if winner is None:
                self.handle_click = self.start_move
            else:
                self.handle_click = self.ignore
                print('Win for %s!' % winner)
        else:
            # Prompt for another move
            self.view.update_view()
            self.handle_click = self.start_move

    def ignore(self, *args):
        pass

    def next_player(self):
        if self.player == X:
            self.player = Y
        else:
            self.player = X

class Square(Button, object):
    def __init__(self, master, x, y):
        Button.__init__(self, master, width=1, border=0, command=self.click)
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
        self['text'] = new

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

if __name__ == '__main__':
    main()
