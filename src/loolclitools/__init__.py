# lool CLI Tools #

'''
    This module brings some tools for building CLIs.
'''

__version__ = '1.0'  # last edit: 10.07.2021

__all__ = ['enable_ANSI_esc_seq', 'getch', 'CursorPosition',
           'get_cursor_position', 'out', 'flush', 'yesno',
           'param', 'vline', 'Selector', 'askinput', 'askpath',
           'console_input', 'notepad_input', 'pause',
           'Timer', 'InteractiveConsole']

from ._main import (
    enable_ANSI_esc_seq, getch, CursorPosition,
    get_cursor_position, out, flush, yesno,
    param, vline, pause, Timer
)

from ._selector import Selector

from ._interactive_console import InteractiveConsole

from ._input import askinput, askpath, console_input, notepad_input
