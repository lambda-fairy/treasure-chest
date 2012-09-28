"""The Treasure Chest model: the 'M' part of MVC"""

from __future__ import print_function

from cStringIO import StringIO
from functools import partial
from itertools import product
import operator
import string
import sys

EMPTY = '.'
X, Y, S, T = ('X', 'Y', 'S', 'T')
PLAYERS = (X, Y)

def isplayer(piece):
    return piece in PLAYERS

def issolid(piece):
    return isplayer(piece) or piece == S

MIN_SIZE, MAX_SIZE = 5, 9

def is_valid_size(size):
    return size % 2 == 1 and MIN_SIZE <= size <= MAX_SIZE

ERROR_TYPES = frozenset([
    'size', 'move_length', 'move_format', 'off_board',
    'supporter_on_treasure', 'overlap', 'groping_empty_space',
    'moving_other_player', 'already_moved', 'move_illegal'
    ])

class InputError(ValueError):
    """Represents a critical failure between desk and chair."""
    def __init__(self, key):
        assert key in ERROR_TYPES
        self.key = key
        super(InputError, self).__init__(key)

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
        output(' ', *string.ascii_uppercase[:self.size])

    def move(self, player, start, end):
        """Move a piece from one point to another.

        If the move ends the game, return the player that won;
        otherwise, return None.

        """
        # Check it's okay with the rule lawyers
        self.check_move(player, start, end)

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

    def valid_moves_from(self, player, start):
        """Get a list of valid moves a player can make from a certain
        start position.

        If there are no such moves, return an empty list.

        """
        valid_ends = []
        for end in product(range(self.size), range(self.size)):
            try:
                self.check_move(player, start, end)
            except InputError:
                pass
            else:
                valid_ends.append(end)
        return valid_ends

    def check_move(self, player, start, end):
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

        if end not in self._project_from(start):
            raise InputError('move_illegal')

    def _project_from(self, start):
        """Given a starting position, project rays in all directions
        until they hit another piece or the edge of the board. Return a
        list of the positions at which they ended."""
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

    def __iter__(self):
        """Allow iterating over the rows of the board."""
        return iter(self.board)

    def __str__(self):
        out = StringIO()
        self.display(file=out)
        return out.getvalue().rstrip() # Annoying trailing newline

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.board)

def make_board(size):
    """Create an initial board of a certain size. The size must be odd."""
    if not is_valid_size(size):
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
    """Return whether a pair represents a valid point on the board."""
    return 0 <= pos[0] < size and 0 <= pos[1] < size
