"""Messages used by the command line interface"""

from model import MIN_SIZE, MAX_SIZE, ERROR_TYPES

# Change this to True if submitting to university
BORING = False

MESSAGES = {
    'prompt_size': "Board size: ",
    'prompt_move': "Player {0}, enter move: ",
    'win': "Win for player {0}!",
    }

ERROR_MOVE_SIZE = "Size must be an odd number between {0} and {1}".format(MIN_SIZE, MAX_SIZE)

if not BORING:
    # Interesting error messages
    ERRORS = {
        'size': ERROR_MOVE_SIZE,
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

else:
    # Boring error messages
    ERROR_MOVE_LENGTH = "Move must be 5 characters"
    ERROR_MOVE_PIECE = "Error move piece"
    ERROR_MOVE_POSITION = "Invalid position"
    ERROR_MOVE_FORMAT = "Invalid input format"
    ERROR_MOVE_ILLEGAL = "Illegal move"

    ERRORS_BORING = {
        'size': "Size must be an odd number between {0} and {1}".format(MIN_SIZE, MAX_SIZE),
        'move_length': ERROR_MOVE_LENGTH,
        'move_format': ERROR_MOVE_FORMAT,
        'off_board': ERROR_MOVE_POSITION,
        'supporter_on_treasure': ERROR_MOVE_POSITION,
        'overlap': ERROR_MOVE_POSITION,
        'groping_empty_space': ERROR_MOVE_PIECE,
        'moving_other_player': ERROR_MOVE_PIECE,
        'already_moved': ERROR_MOVE_PIECE,
        'move_illegal': ERROR_MOVE_ILLEGAL,
        }

assert ERROR_TYPES == set(ERRORS.keys())
