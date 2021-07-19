# lool CLI Tools #

"""
    This file contains the getpass functions.
"""

from ._main import out, getch

from sys import stdout
from msvcrt import kbhit


def getpass(prompt: str = "Password: ", mask: str = "*") -> str:

    if not isinstance(prompt, str):
        raise TypeError("prompt must be a string")
    if not isinstance(mask, str):
        raise TypeError("mask must be a string")
    if not len(mask) == 1:
        raise ValueError("mask must have a length of 1")

    pswd: list[str] = []

    out(prompt, flush=True)

    while True:
        key = getch()

        if key in (b"\r", b"\n"):
            out("\n", flush=True)
            return "".join(pswd)

        elif key == b"\b":
            stdout.write("\b \b")
            stdout.flush()
            pswd.pop()
            continue

        elif key in (b"\xe0", b"\x00") and kbhit():
            key = getch()
            if key == b"S":  # DEL
                continue
            elif key == b"H":  # UP
                continue
            elif key == b"P":  # DOWN
                continue
            elif key == b"K":  # LEFT
                continue
            elif key == b"M":  # RIGHT
                continue
            elif key == b"R":  # INSERT
                continue
            elif key == b"G":  # POS1
                continue
            elif key == b"O":  # ENDE
                continue
            elif key == b"I":  # PAGE UP
                continue
            elif key == b"Q":  # PAGE DOWN
                continue
            elif key in (b";", b"<", b"=", b">", b"?", b"@", b"A", b"B", b"C", b"D", b"\x85", b"\x86"):  # F-KEYS
                continue

        # elif ord(key) <= 0x1F or 0x80 <= ord(key) <= 0xA0:  # unprintable
        #     stdout.write(".")
        #     stdout.flush()
        #     continue

        stdout.write("*")
        stdout.flush()

        try:
            pswd.append(key.decode())
        except UnicodeDecodeError:
            while kbhit():
                key += getch()
            pswd.append(key.decode())
