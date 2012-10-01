#!/usr/bin/env python

from datetime import datetime
import omnipack

now = datetime.utcnow().replace(microsecond=0)

PROLOGUE = '''
----------------
 Treasure Chest
----------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||

:Author: Chris Wong
:Version: {datetime}

This is an implementation of the simple board game, **Treasure Chest**,
packed into a single file.

The full source code for this program is available at:

    https://github.com/lfairy/treasure-chest
'''.format(datetime=now.isoformat())

FILES = '''
resources/chest.gif
resources/boat_r.gif
resources/boat_b.gif
resources/buoy.gif
resources/blank.gif
treasurelib/gui/__init__.py
treasurelib/gui/messages.py
treasurelib/gui/resources.py
treasurelib/gui/tk_aboutbox.py
treasurelib/gui/tk_hyperlink.py
treasurelib/gui/tk_util.py
treasurelib/model.py
treasurelib/__init__.py
'''.strip().split()

def main():
    sources = {}
    for name in FILES:
        sources[name] = open(name).read()

    entry = 'from treasurelib import gui; gui.main()'

    with open('treasureChestgui.py', 'w') as outfile:
        omnipack.pack(PROLOGUE, sources, entry, outfile)

if __name__ == '__main__':
    main()
