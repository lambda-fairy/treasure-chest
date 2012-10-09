"""Loads and caches images used by the GUI."""

from base64 import b64encode
from functools import wraps
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

def memoize(f):
    cache = {}
    @wraps(f)
    def newf(*args):
        try:
            return cache[args]
        except KeyError:
            result = f(*args)
            cache[args] = result
            return result
    return newf

@memoize
def load_image(key):
    name = NAMES[key]
    data = read_resource(name)
    return PhotoImage(data=b64encode(data))

def read_resource(name):
    name = os.path.join('resources', name)
    with open(name) as f:
        return f.read()
