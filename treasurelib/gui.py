#!/usr/bin/env python
"""Treasure Chest GUI using Tkinter."""

from __future__ import print_function

from Tkinter import *
import tkMessageBox

from model import Board, EMPTY

COPYRIGHT = u'''
\xA9 2012 Chris Wong.

I like shorts, they are comfortable and easy to wear.
'''.strip()

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
        self.squares = None

    def restart(self, size):
        self.commit_infanticide()
        self.board = Board(size)

        self.squares = []
        for y in range(size):
            row = []
            for x in range(size):
                row.append(Square(self, x, y))
            self.squares.append(row)

        self.display()

    def display(self):
        for brow, srow in zip(self.board, self.squares):
            for piece, square in zip(brow, srow):
                square.piece = piece

    def commit_infanticide(self):
        if self.squares is not None:
            for row in self.squares:
                for child in row:
                    child.destroy()
            self.squares = None

class Square(Button, object):
    def __init__(self, master, x, y):
        Button.__init__(self, master, width=1)
        self.piece = EMPTY
        self.grid(row=y, column=x)
        self['command'] = lambda: print('Clicked', self.piece)

    def get_piece(self):
        return self._piece

    def set_piece(self, new):
        self._piece = new
        self['text'] = new

    piece = property(get_piece, set_piece)

    def placate(self):
        self['background'] = None

if __name__ == '__main__':
    main()
