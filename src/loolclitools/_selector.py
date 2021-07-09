# lool CLI Tools #

import sys
import os
from ._main import getch, flush
from typing import List


class Selector:  # use sys.stdout.write instead of out here for performance reasons
    def __init__(self, entries: List[str], title: str = None, select: str = ">", print_result: bool = True, start_pos: int = None):
        """`entries` - Each None or "" will be a blank line."""

        # replace "" with None; None means empty line
        entries = tuple(i or None for i in entries)
        # remove all empty lines (None)
        self.entries = tuple(i for i in entries if i)
        self.title = title
        self.select = (" " if self.title is not None else "") + \
            select  # add space if title is used; looks better
        self.__highest_index = len(self.entries)-1
        self.__entry_prefix = f"\x1b[{len(self.select) + 3}C"
        self.__title_end = f"\x1b[A\x1b[{len(title) + 3}C" if title is not None else "\x1b[2C"
        self.__empty_line_indexes = set()
        entries = list(entries)
        # not possible with list/set comprehension: indexes and size have to change during iteration
        for _ in range(entries.count(None)):
            self.__empty_line_indexes.add(entries.index(None) - 1)
            entries.remove(None)
        self.pos = self.prev = 0
        self.__prev_terminal_size = os.get_terminal_size().lines

        sys.stdout.write("\x1b[0m\x1b[?25l")

        if title is not None:
            sys.stdout.write(f"\x1b[2C{title}\n")

        self.__init_options()

        if start_pos:
            self.pos = start_pos
            self.__update()

        while True:
            self.__update()
            char = getch()

            if char in (b"\xe0", b"\x00"):  # xe0 e.g. conhost, x00 e.g. VS integrated shell, OpenSSH
                char = getch()
                if char == b'H':
                    self.__up()  # arrow up
                elif char == b'P':
                    self.__down()  # arrow down
                self.__update()

            elif char == b"w":
                self.__up()
            elif char == b"s":
                self.__down()

            # numbers
            elif char in b"123456789":
                if self.__select_element(int(char)):  # pos was changed
                    break

            elif char == b"\r":  # enter
                break

            elif char in (b"\x03", b"\x1b"):  # CTRL+C, ESC
                sys.stdout.write("\x1b[?25h\x1b[u")
                sys.stdout.write(f"\x1b[J{self.__title_end}\x1b[91mcanceled\x1b[0m\n" if print_result else (
                    f"\x1b[A\x1b[J" if title is not None else f"\x1b[J"))
                flush()
                raise KeyboardInterrupt

        # exit Selector
        self.result = self.entries[self.pos]
        sys.stdout.write("\x1b[u\x1b[?25h")
        if print_result:
            sys.stdout.write(
                f"\x1b[J{self.__title_end}\x1b[96m{self.entries[self.pos]}\x1b[0m\n")
        else:
            sys.stdout.write(
                f"\x1b[A\x1b[J" if title is not None else f"\x1b[J")
            flush()  # no new line at the end so flushing is required

    def __up(self) -> None:
        self.pos = self.__highest_index if self.pos == 0 else self.pos - 1

    def __down(self) -> None:
        self.pos = 0 if self.pos == self.__highest_index else self.pos + 1

    def __select_element(self, num) -> bool:
        # 0th position == 1st element
        if num - 1 <= self.__highest_index:
            self.pos = num - 1
            return True  # return True if position was changed
        return False

    def __init_options(self) -> None:
        sys.stdout.write("\r\x1b[s")
        flush()
        for i, entry in enumerate(self.entries):
            sys.stdout.write(f"{self.__entry_prefix}\x1b[0m{entry}\n")
            if i in self.__empty_line_indexes:
                sys.stdout.write("\n")
        sys.stdout.write("\x1b[u")

    def __update(self) -> None:
        if self.__prev_terminal_size != os.get_terminal_size().lines:
            sys.stdout.write("\x1b[J")
            self.__init_options()
            sys.stdout.write("\x1b[u")

        if self.prev > 0:  # go to previous position
            sys.stdout.write(f"\x1b[{self.__real_pos(self.prev)}B")
        # print unselect position
        sys.stdout.write(
            f"{self.__entry_prefix}\x1b[1K\x1b[0m{self.entries[self.prev]}")

        sys.stdout.write("\x1b[u")
        if self.pos > 0:  # go to selected position
            sys.stdout.write(f"\x1b[{self.__real_pos(self.pos)}B")
        # print selected position
        sys.stdout.write(
            f"  \x1b[97m{self.select} \x1b[96m{self.entries[self.pos]}\x1b[0m")

        sys.stdout.write(f"\x1b[u")
        flush()
        self.prev = self.pos
        self.__prev_terminal_size = os.get_terminal_size().lines

    # calculate real position in console with empty lines
    def __real_pos(self, pos: int) -> int:
        # adds up bools so ones and zeros
        return (pos + sum(i < pos for i in self.__empty_line_indexes)) if self.__empty_line_indexes else pos

    def __eq__(self, obj: object) -> bool:
        return obj == self.pos
