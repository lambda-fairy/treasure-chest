"""Exports a ``Hyperlink`` class, for creating clickable links."""

from Tkinter import Label
import webbrowser

from .tk_util import modify_font

class Hyperlink(Label):
    def __init__(self, master, destination=None, text=None):
        Label.__init__(
                self, master, text=(text or destination or ''),
                foreground='#0000ff')
        modify_font(self, underline=True)

        self.destination = destination

        self.bind('<1>', self.click_link)
        self.bind('<Enter>', self._enter)
        self.bind('<Leave>', self._leave)

    def _enter(self, event):
        self['cursor'] = 'hand2'

    def _leave(self, event):
        self['cursor'] = None

    def click_link(self, event):
        if self.destination:
            webbrowser.open(self.destination)
