"""Messages used by the graphical interface"""

from ..model import X, Y

MESSAGES = {
        'prompt_move': lambda player: '{0}, make your move'.format(NAMES[player]),
        'win': lambda player: '{0} wins!'.format(NAMES[player]),
        'board_size': 'Board size',
        }

NAMES = {
    X: 'Red',
    Y: 'Blue',
    }
