import os
import sys
import socket
import colorama
from .methods import Methods
from .basic import Lexer, Interpreter

class Term(object):
    def __init__(self):
        self.user = os.getlogin()
        self.pc = socket.gethostname()
        self.color = colorama.Fore.GREEN
        self.c_reset = colorama.Style.RESET_ALL
        self.intro = ("Welcome to the pwterm.\n"
                      "Type 'help' to see the available commands.")
        self.methods = Methods()

    def run(self):
        print(self.intro)
        while True:
            try:
                entry = input(f"{self.color}{self.user}@{self.pc}{self.c_reset}:")
                if self.methods.run_method(entry.split()):
                    continue
                else:
                    lexer = Lexer(entry)
                    interpreter = Interpreter(lexer)
                    result = interpreter.interpret()
                    print(result)
            except Exception as e:
                # noinspection PyUnboundLocalVariable
                print(f"Error: {e}.")
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt: Exiting the terminal...")
                sys.exit()