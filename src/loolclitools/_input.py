# lool CLI Tools #

'''
    This file includes functions that can be used
    to get input from the user.
'''

import os
from io import BufferedReader
from ._main import out, flush, getch, vline, get_cursor_position
from ._getpass import getpass
from typing import Optional


NOTEPAD_PATH = os.path.join(os.getenv('windir'), 'System32', 'notepad.exe')


# -----==============-----
#      ADVANCED INPUT
# -----==============-----
def askinput(prompt: str = '', is_password: bool = False) -> str:
    '''
        A function for getting input from the user.
        If `is__password` is True the input will be masked with '*'.
    '''
    out('\x1b[0m')
    try:
        result = (getpass if is_password else input)(
            f'\x1b[2C{prompt}\x1b[96m')
    except (KeyboardInterrupt, EOFError):
        # when keybintrpt is thrown 'canceled' message is prefixed with \x1b[2C therfore first moving back (\x1b[2D)
        out('\x1b[J\x1b[0m\x1b[2D')
        raise KeyboardInterrupt
    else:
        out('\x1b[0m')
        flush()
        return result


# -----==========-----
#      PATH INPUT
# -----==========-----
def askpath(prompt: str, /, must_be_file: bool = False, must_be_dir: bool = False) -> str:
    '''
        A function for getting a path from the user.

        If `must_be_file` is True only files are accepted.
        If `must_be_dir` is True only directories are accepted.
    '''
    out('\x1b[0m\x1b[s')
    def err(msg): return out(
        f'\x1b[B\x1b[2C\x1b[J\x1b[91m{msg}\x1b[0m\x1b[u\x1b[K')
    while True:
        filepath = askinput(prompt)
        # remove ' and ' from start and end
        if filepath and filepath[0] in (''', ''') and filepath[-1] in (''', '''):
            filepath = filepath[1:-1]
        # validate
        if not filepath:
            out('\x1b[A\x1b[K')
            continue
        elif not os.path.exists(filepath):
            err(f'This ' + ('file' if must_be_file else 'directory' if must_be_dir else 'path') + ' does not exist!')
        elif must_be_file and not os.path.isfile(filepath):
            err(f'The specified path is not a file!')
        elif must_be_dir and not os.path.isdir(filepath):
            err(f'The specified path is not a directory!')
        else:
            out('\x1b[0m\x1b[J')
            return filepath


# -----=============-----
#      CONSOLE INPUT
# -----=============-----
def console_input(header: str = None, alt_buf: bool = True) -> str:
    '''
        A function for getting multi line input from the user inside the console.

        If `alt_buf` is False, no alternative buffer will be created.
        This should only be used e.g. in loops, where still an alternative buffer is created, before
        the loop, and exited after the loop. This is useful because instead each time console_input
        is called the alternative buffer would be destroyed and recreated, which is not necessary.
    '''

    if alt_buf:
        out('\x1b[?1049h', flush=True)

    begin = get_cursor_position().y

    def HEADER(): return ''.join((f'\x1b[s\x1b[{begin}H', vline(), ('\n  ' + '\n  '.join(header.splitlines()) + '\n') if header else '',
                                  '\n  \x1b[93mPress F6 and then Enter in an empty line or CTRL+C to finish.\x1b[0m\n', vline(), '\x1b[u'))

    start_pos = HEADER().count('\n') + begin + 2
    out(f'\x1b[{start_pos}H', flush=True)

    text = []
    prev_pos = None
    try:
        while True:
            if prev_pos != os.get_terminal_size():
                out(f'\x1b[s\x1b[{start_pos}H\x1b[1J\x1b[u', HEADER(
                ), f'\x1b[{start_pos};{os.get_terminal_size().lines-1}r\x1b[u')
                prev_pos = os.get_terminal_size()
            text.append(input('\x1b[2C'))
    except (KeyboardInterrupt, EOFError):
        pass

    out('\x1b[?1049l' if alt_buf else (f'\n{vline()}\n\n'), flush=True)
    return '\n'.join(text)


# -----=============-----
#      NOTEPAD INPUT
# -----=============-----
def notepad_input(filename: str, header: Optional[str] = None, suffix: str = '.txt', data: Optional[bytes] = None, notepad_path: os.PathLike = NOTEPAD_PATH) -> BufferedReader:
    '''
        A function for getting input from the user using the notepad application.

        This will only work on Windows.
    '''

    from subprocess import Popen, CREATE_NEW_CONSOLE, CREATE_BREAKAWAY_FROM_JOB, TimeoutExpired
    from tempfile import mktemp

    start_pos = get_cursor_position().y

    file = mktemp(prefix=filename + '_', suffix=suffix)
    with open(file, 'wb') as f:
        if data:
            f.write(data)

    out('\x1b[?25l')

    if header:
        out(vline(), '\n\n  ', '\n  '.join(header.splitlines()), '\n\n\x1b[0m')

    out(vline(), '\n\n\x1b[s'
        '  \x1b[93mWaiting for notepad to terminate . . .\n\n'
        f'  \x1b[0mFilename: \x1b[96m%temp%\\{os.path.split(file)[1]}\n\n'
        '  \x1b[90mPress CTRL+C to force continue.\n\n\x1b[0m', vline(),
        flush=True)

    process = Popen([notepad_path, file],
                    creationflags=CREATE_NEW_CONSOLE | CREATE_BREAKAWAY_FROM_JOB)
    try:
        # if this fails, the process terminated within the 500 ms
        process.wait(.5)
    except TimeoutExpired:  # but when the timeout expires, this loop waits for the process to finish but alo listens for CTRL+C
        while True:
            try:
                process._wait(.25)
            except TimeoutExpired:
                continue
            except KeyboardInterrupt:
                break
            else:
                break
    else:
        out('\x1b[u\x1b[4B\x1b[K  \x1b[90mThe process terminated too quickly, assuming the file was handeled in another instance.'
            '\x1b[u\x1b[K  \x1b[93mPress any key to continue . . . \x1b[?25h', flush=True)
        getch()
    finally:
        out(f'\x1b[{start_pos}H\x1b[J\x1b[?25h', flush=True)

    return open(os.open(file, os.O_RDONLY | os.O_BINARY | os.O_TEMPORARY), 'rb')
