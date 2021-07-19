# lool CLI Tools #

"""
    This file contains all the small components of loolclitools.
"""

import sys
import os
from getpass import getpass
from time import perf_counter
from msvcrt import getch as _getch, kbhit
from typing import Any, NamedTuple


# -----=======================-----
#      INITIALIZATION FUNCTION
# -----=======================-----
def enable_ANSI_esc_seq() -> None:
    """
    This function enables ANSI escape sequences inside the current console.
    """
    from ctypes import cdll, c_ulong, POINTER

    kernel32 = cdll.kernel32
    handle = kernel32.GetStdHandle(c_ulong(-11))
    mode = POINTER(c_ulong)(c_ulong(0))
    kernel32.GetConsoleMode(handle, mode)
    kernel32.SetConsoleMode(handle, c_ulong(4 | mode.contents.value))


enable_ANSI_esc_seq()


# -----==============-----
#      MODIFIED GETCH
# -----==============-----
def getch() -> bytes:
    """
    Just like msvcrt.getch but pressing CTRL+I + CTRL+C will start an interactive console.
    """
    char = _getch()
    from ._interactive_console import InteractiveConsole

    if char == b"\x09" and _getch() == b"\x03":  # CTRL + I and CTRL + C
        InteractiveConsole()
    else:
        InteractiveConsole.temporary_globals.clear()
    return char


# -----===============-----
#      CURSOR POSITION
# -----===============-----
class CursorPosition(NamedTuple):
    x: int
    y: int

    def apply(self):
        out(f"\x1b[{self.y};{self.x}H")


def get_cursor_position() -> CursorPosition:
    data = []
    print(end="\x1b[6n", flush=True)
    while (char := _getch()) != b"R":
        if not char in (b"\x1b", b"["):
            data.append(char)
    return CursorPosition(*map(int, reversed(b"".join(data).split(b";"))))


# -----================-----
#      OUTPUT FUNCTIONS
# -----================-----
def out(*text: Any, sep: str = "", flush: bool = False) -> None:
    """
    Just like sys.stdout.write() but with a bit more functionality.
    """
    sys.stdout.write(sep.join(map(str, text)))
    if flush:
        sys.stdout.flush()


def flush() -> None:
    sys.stdout.flush()


# -----=========================-----
#      ADVANCED OUTPUT FUNCTIONS
# -----=========================-----
def yesno(obj: object) -> str:
    """
    Convert an object into 'Yes' or 'No'.
    """
    return "Yes" if obj else "No"


def param(name: str, value: str, ljust: int = None) -> None:
    """
    Print a key and a value formatted in a specific way.
    """
    name += ": "
    if ljust:
        name = name.ljust(ljust)
    out(f"\x1b[0m\x1b[2C{name}\x1b[96m{value}\x1b[0m\n")


def vline() -> str:
    """
    Returns a vertical line that is as long as the console currently is.
    """
    return "\x1b(0" + "q" * (os.get_terminal_size().columns - 1) + "\x1b(B"


# -----=====-----
#      PAUSE
# -----=====-----
def pause():
    """
    Pause the program, clean up some things and exit.
    """
    out("\n\x1b[0mPress any key to exit . . . ")
    flush()
    while kbhit():
        getch()  # discard waiting input
    getch()
    out("\x1b!p\n")
    flush()


# -----=====-----
#      TIMER
# -----=====-----
class Timer:
    """
    This class can be used to measure time in a convenient way.
    """

    time = 0.0

    def start(self):
        self.__start = perf_counter()

    def stop(self) -> float:
        t = self.__start - perf_counter()
        self.time += t
        return t
