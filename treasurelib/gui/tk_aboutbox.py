"""Exports an ``AboutBox`` class, for creating GTK-style about boxes."""

from tkinter import Button, Frame, Label, ACTIVE, RIGHT
from tkinter.font import BOLD
from tkinter.simpledialog import Dialog

from .tk_hyperlink import Hyperlink
from .tk_util import modify_font

class AboutBox(Dialog):
    def __init__(self, master, app_name, description=None, copyright=None, website=None):
        self.app_name = app_name
        self.description = description
        self.copyright = copyright
        self.website = website

        Dialog.__init__(self, master)

    def body(self, master):
        if self.app_name:
            self.title(self.app_name)
            label = Label(master, text=self.app_name)
            modify_font(label, size=12, weight=BOLD)
            label.pack()

        if self.description:
            label = Label(master, text=self.description)
            modify_font(label, size=10)
            label.pack(pady=10)

        if self.copyright:
            label = Label(master, text=self.copyright)
            modify_font(label, size=8)
            label.pack()

        if self.website:
            label = Hyperlink(master, destination=self.website)
            modify_font(label, size=8)
            label.pack()

    def buttonbox(self):
        box = Frame(self)

        w = Button(box, text="Close", width=8, command=self.ok, default=ACTIVE)
        w.pack(side=RIGHT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side=RIGHT)
