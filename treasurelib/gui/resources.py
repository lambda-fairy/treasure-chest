"""A simple class that loads and caches images."""

import os
from Tkinter import PhotoImage

from ..model import EMPTY, S, T, X, Y

NAMES = {
    EMPTY: 'blank.gif',
    S: 'buoy.gif',
    T: 'chest.gif',
    X: 'boat_r.gif',
    Y: 'boat_b.gif',
    }

class ResourceManager:
    def __init__(self):
        self.pics = {}

    def load(self, key):
        name = NAMES[key]
        try:
            return self.pics[name]
        except KeyError:
            pic = PhotoImage(file=get_file_name(name))
            self.pics[name] = pic
            return pic

def get_file_name(name):
    return os.path.join('resources', name)
