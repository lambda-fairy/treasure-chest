"""Miscellaneous utilities for working with Tkinter."""

from tkFont import Font

def modify_font(widget, **attrs):
    """Change the font used by a widget, by applying the given
    attributes to it.

    For example, you can make a label bold using::

        modify_font(label, weight=tkFont.BOLD)

    """
    font = Font(widget, widget['font'])
    for key, value in attrs.items():
        font[key] = value
    widget['font'] = font
