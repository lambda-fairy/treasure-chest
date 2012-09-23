#!/usr/bin/env python
"""Simple command line interface"""

from __future__ import print_function

from itertools import cycle
import string

from model import Board, InputError, PLAYERS, is_valid_size
import messages as M

def play(board_cfg=None):
    """Play a game of Treasure Chest on the command line, optionally
    with an initial board state."""

    # Initialize the board
    if board_cfg is None:
        size = read_with(parse_size, 'prompt_size')
        board = Board(size)
    else:
        board = Board(board_cfg)

    # Play the game
    winner = None
    for player in cycle(PLAYERS):
        # Word of God dictates the board shall henceforth be surrounded
        # by blank lines
        print()
        board.display()
        print()

        # Stop if we have a winner
        if winner is not None:
            break

        # Read the next move and execute it in one go
        def parse_and_move(s):
            start, end = parse_move(s)
            return board.move(player, start, end)
        winner = read_with(parse_and_move, 'prompt_move', player)

    # Burma Shave
    print(M.MESSAGES['win'].format(winner))

def read_with(reader, key, *args):
    """Prompt the user for input, then pass the resulting string to the
    reader function. If it raises an InputError, display the error and
    prompt again."""
    message = M.MESSAGES[key].format(*args)
    while True:
        try:
            return reader(raw_input(message).strip())
        except InputError as ex:
            print(M.ERRORS[ex.key])

def parse_size(s):
    try:
        size = int(s)
    except ValueError:
        raise InputError('size')

    if is_valid_size(size):
        return size
    else:
        raise InputError('size')

def parse_move(s):
    """Parse a move: a string in the form ``A1:Z2`` specifying a start
    and end position."""
    if len(s) != 5:
        raise InputError('move_length')

    parts = s.split(':')
    if len(parts) != 2:
        raise InputError('move_format')

    return map(parse_position, parts)

def parse_position(s):
    """Parse a position: a string in the form ``P9`` that specifies a
    location on the board."""
    if len(s) != 2 or not s[0].isalpha() or not s[1].isdigit():
        raise InputError('move_format')

    return string.ascii_uppercase.index(s[0].upper()), int(s[1]) - 1

if __name__ == '__main__':
    play()
