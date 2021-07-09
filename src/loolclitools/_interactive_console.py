# lool CLI Tools #

from ._main import out, vline
from codeop import CommandCompiler
from pprint import pprint
from typing import Optional


class InteractiveConsole:
    """`permanent_globals`: these items will be available in each interactive console
    `temporary_globals`: these items will be only available within the next interactive console
    If `temporary_globals` is changed before calling loolclitools.getch(), no matter if an
    interactive console was started or not, the dictionary will be cleared."""

    permanent_globals = {}
    temporary_globals = {}

    def __init__(self, g: Optional[dict] = None):

        self.compile = CommandCompiler()

        # create globals
        self.g = g or {}
        self.g.update(self.permanent_globals)
        self.g.update(self.temporary_globals)
        self.temporary_globals.clear()
        self.g.update({
            "__name__": "__main__",
            "__loader__": __loader__,
            "__builtins__": self.__builtins()
        })

        self._init()

        # main loop
        self.mainloop = True
        while self.mainloop:

            # get input
            try:
                self.cmd = input("\x1b[0m>>> ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            out("\x1b[0m", flush=True)

            # validate input, check for custom commands
            if not self.cmd:
                out("\r\x1b[A")
                continue

            elif self.cmd == "!help":
                out("\n"
                    "  \x1b[92mList of all custom commands:\n\n"
                    "   \x1b[0m- \x1b[97mcls, clear            \x1b[90mclears the screen\n"
                    "   \x1b[0m- \x1b[97mexit, quit            \x1b[90mexits\n"
                    "   \x1b[0m- \x1b[97m!rerender             \x1b[90museful if console was resized; may solve issues with scrolling then\n"
                    "   \x1b[0m- \x1b[97m!reload               \x1b[90mrestart whole interactive console\n"
                    "\n  \x1b[90mAlso try using pprint() or pp() instead of the print() function.\n")

            elif self.cmd in ("cls", "clear"):
                out("\x1b[7H\x1b[J\x1b[6H", flush=True)

            elif self.cmd == "!rerender":
                out("\x1b[?1049l")
                self._init()
                continue

            elif self.cmd == "!reload":
                out("\x1b[?1049l")
                InteractiveConsole()
                return

            elif self.cmd in ("exit", "quit"):
                break

            else:  # execute
                self._execute()

            # end of each loop iteration
            out("\n")

        # end of init
        out("\x1b!p\x1b[?1049l", flush=True)

    @staticmethod
    def _init():
        out("\x1b[?1049h\x1b[94m", vline(), "\x1b[97m\n\n  Interactive Console\n\x1b[90m  CTRL+C to exit, '!help' for help.\n\n\x1b[94m",
            vline(), "\x1b[0m\n\x1b[7;r\x1b[7H", flush=True)

    def _execute(self):
        try:  # execution
            code = self.compile(self.cmd, "<input>", "single")

            if code is None:  # more input needed
                self.cmd += "\n" + input("\x1b[0m... ")
                self._execute()
                return

            exec(code, self.g)

        except SystemExit:
            self.mainloop = False

        except BaseException as exc:
            out("\x1b[91m", type(exc).__name__, f"\x1b[90m:\x1b[0m {exc.args[0]}" if len(
                exc.args) > 0 else "", "\x1b[0m\n")

    def __builtins(self) -> object:
        builtins = __import__("builtins")  # forced re-import

        builtins.pprint = builtins.pp = pprint

        def exit():
            self.mainloop = False
        builtins.exit = builtins.quit = exit

        return builtins
