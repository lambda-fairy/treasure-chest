"""Omnipack: bundle a whole project into a single Python source file."""

from __future__ import print_function

import base64
import cPickle as pickle
from functools import partial
import os
import zlib

template = open(os.path.join(os.path.dirname(__file__), 'template.in')).read()

def pack(prologue, sources, entry, outfile):
    """Bundle the given source files and write the result to a file object."""
    encoded_sources = base64.encodestring(zlib.compress(pickle.dumps(sources)))
    write = partial(print, file=outfile, sep='\n')
    write('#!/usr/bin/env python')
    write('"""', prologue, '"""')
    write('sources = """', encoded_sources, '"""')
    write('entry = """', entry, '"""')
    outfile.write(template)
