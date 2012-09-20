#!/usr/bin/env python
"""The Treasure Chest model: the 'M' part of MVC"""

from __future__ import print_function

from cStringIO import StringIO
from functools import partial
from itertools import cycle
import operator
import sys

EMPTY = '.'
X, Y, S, T = ('X', 'Y', 'S', 'T')

MIN_SIZE, MAX_SIZE = 5, 9

def isplayer(piece):
    return piece in (X, Y)

def issolid(piece):
    return isplayer(piece) or piece == S

MESSAGES = {
        'prompt_size': "Board size: ",
        'prompt_move': "Player {0}, enter move: ",
        'win': "Win for player {0}!",
        }

ERRORS = {
        'size': "Size must be an odd number between {0} and {1}".format(MIN_SIZE, MAX_SIZE),
        'move_length': "Input must be in the format A1:B2",
        'move_format': "Input must be in the format A1:B2",
        'off_board': "You try to go off the board, but that just shows how far you've gone off the rails.",
        'supporter_on_treasure': "You can't move a supporter piece onto the treasure, you saucy boy.",
        'overlap': "You can't move a piece on top of another one.",
        'groping_empty_space': "You grope madly at the patch of empty space, to no avail.",
        'moving_other_player': "You can't move the other player. Jerk.",
        'already_moved': "You can't move the piece that was moved last.",
        'move_illegal': "You must move the as far as possible horizontally, vertically or diagonally.",
        }

class InputError(ValueError):
    """Represents a critical failure between desk and chair."""
    def __init__(self, key):
        message = ERRORS[key]
        super(InputError, self).__init__(message)

# The letters of the alphabet from A to Z
letters = [chr(x) for x in range(ord('A'), ord('Z')+1)]

class Board:
    """Represents a game of Treasure Chest."""

    def __init__(self, board_or_size=5):
        """Start a game.

        If the argument is a nested list, it will be used as the initial
        game state; if it is an integer, a new board will be created of
        that size.

        """
        try:
            self.board = list(board_or_size)
            self.size = len(self.board)
        except TypeError:
            self.board = make_board(board_or_size)
            self.size = board_or_size
        self.last_move = None

    def display(self, file=sys.stdout):
        """Write a human-readable representation of the board to the
        screen."""
        output = partial(print, file=file)
        for y, row in enumerate(self.board, 1):
            output(y, *row)
        output(' ', *letters[:self.size])

    def move(self, player, start, end):
        """Move a piece from one point to another.

        If the move ends the game, return the player that won;
        otherwise, return None.

        """
        # Check it's okay with the rule lawyers
        self._check_move(player, start, end)

        # Move the piece, bra
        src, dest = self.get(start), self.get(end)
        self.set(start, EMPTY)
        self.set(end, src)
        self.last_move = end

        # If a player moves onto the T, they win!
        if isplayer(src) and dest == T:
            assert player == src
            return player
        else:
            return None

    def _check_move(self, player, start, end):
        """If the move is valid, do nothing; if it is invalid, raise an
        InputError."""
        if (not in_board(start, self.size) or
                not in_board(end, self.size)):
            raise InputError('off_board')

        src, dest = self.get(start), self.get(end)

        if src == S and dest == T:
            raise InputError('supporter_on_treasure')

        if not issolid(src):
            raise InputError('groping_empty_space')

        if issolid(dest):
            raise InputError('overlap')

        if isplayer(src) and player != src:
            raise InputError('moving_other_player')

        if start == self.last_move:
            raise InputError('already_moved')

        if end not in self._valid_moves_from(start):
            raise InputError('move_illegal')

    def _valid_moves_from(self, start):
        """Given a starting position, return a list of valid moves the
        player can make from there."""
        results = []
        for delta in [(-1, -1), (-1, 0), (-1, 1),
                      ( 0, -1),          ( 0, 1),
                      ( 1, -1), ( 1, 0), ( 1, 1)]:
            # Find the farthest destination in each direction
            farthest = self._find_farthest(start, delta)
            if farthest is not None:
                results.append(farthest)
        return results

    def _find_farthest(self, start, delta):
        """Find the farthest position a piece can move to in a certain
        direction.

        If there is no valid move in that direction, return None.

        """
        src = self.get(start)
        farthest = None
        for end in project_ray(start, delta):
            if not in_board(end, self.size):
                # We're off the board! Noooooooooo!
                break

            dest = self.get(end)
            # If the destination is occupied, we can't go any further
            if dest not in (T, EMPTY):
                break

            # A Supporter can't land on the treasure chest, but it can
            # still land past it -- hence the lack of `break`.
            if not (src == S and dest == T):
                farthest = end

        return farthest

    def get(self, pos):
        x, y = pos
        return self.board[y][x]

    def set(self, pos, piece):
        x, y = pos
        self.board[y][x] = piece

    def __str__(self):
        out = StringIO()
        self.display(file=out)
        return out.getvalue().rstrip() # Annoying trailing newline

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.board)

def make_board(size):
    """Create an initial board of a certain size. The size must be odd."""
    if size < 3 or not odd(size):
        raise ValueError('invalid size: {0}'.format(size))

    board = matrix((size, size), default=EMPTY)
    mid = size // 2

    # X player
    board[0] = [S] * size
    board[0][mid] = X

    # Y player
    board[-1] = [S] * size
    board[-1][mid] = Y

    # Treasure chest
    board[mid][mid] = T

    return board

def odd(n):
    return n % 2 == 1

def matrix(sizes, default=None):
    """Make a nested list, filled with a default value."""
    if sizes:
        head, tail = sizes[0], sizes[1:]
        return [matrix(tail, default) for i in range(head)]
    else:
        return default

def project_ray(start, delta):
    """Yield a stream of values obtained by repeatedly adding an offset
    to a start point."""
    current = start
    while True:
        current = current[0] + delta[0], current[1] + delta[1]
        yield current

def add_tuple(xs, ys):
    """Add the corresponding elements of two tuples. Both arguments
    should be the same length."""
    return tuple(map(operator.add, xs, ys))

def in_board(pos, size):
    return 0 <= pos[0] < size and 0 <= pos[1] < size


# ======================================================================
# Main game loop
# ----------------------------------------------------------------------

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
    for player in cycle((X, Y)):
        # Word of God dictates the board shall henceforth be surrounded
        # by blank lines
        print()
        board.display()
        print()

        # Read the next move and execute it in one go
        def parse_and_move(s):
            start, end = parse_move(s)
            return board.move(player, start, end)
        winner = read_with(parse_and_move, 'prompt_move', player)

        # Stop if we have a winner
        if winner is not None:
            break

    # Burma Shave
    print(MESSAGES['win'].format(winner))

def read_with(reader, key, *args):
    """Prompt the user for input, then pass the resulting string to the
    reader function. If it raises an InputError, display the error and
    prompt again."""
    message = MESSAGES[key].format(*args)
    while True:
        try:
            return reader(raw_input(message).strip())
        except InputError as ex:
            print(ex.message)

def parse_size(s):
    try:
        size = int(s)
    except ValueError:
        raise InputError('size')

    if odd(size) and MIN_SIZE <= size <= MAX_SIZE:
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

    return letters.index(s[0].upper()), int(s[1]) - 1

if __name__ == '__main__':
    play()
