# lool CLI Tools #

"""
    This module brings some tools for building CLIs.
"""

__version__ = "1.0.1"  # last edit: 20.07.2021

__all__ = [
    "enable_ANSI_esc_seq",
    "getch",
    "CursorPosition",
    "get_cursor_position",
    "out",
    "flush",
    "yesno",
    "param",
    "vline",
    "Selector",
    "askinput",
    "askpath",
    "console_input",
    "notepad_input",
    "getpass",
    "pause",
    "Timer",
    "InteractiveConsole",
]

from ._main import (
    enable_ANSI_esc_seq,
    getch,
    CursorPosition,
    get_cursor_position,
    out,
    flush,
    yesno,
    param,
    vline,
    pause,
    Timer,
)

from ._selector import Selector

from ._interactive_console import InteractiveConsole

from ._input import askinput, askpath, console_input, notepad_input

from ._getpass import getpass


# -----=========-----
#      AUTO INIT
# -----=========-----
enable_ANSI_esc_seq()

# set code page to UTF-8
try:
    from ctypes import windll
except (ImportError, ModuleNotFoundError):
    pass
else:
    windll.kernel32.SetConsoleCP(65001)
