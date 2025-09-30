"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from colorama import Fore, Style, init

init(autoreset=True)

GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW

LIGHTBLACK_EX = Fore.LIGHTBLACK_EX
LIGHTYELLOW_EX = Fore.LIGHTYELLOW_EX
LIGHTBLUE_EX = Fore.LIGHTBLUE_EX
LIGHTCYAN_EX = Fore.LIGHTCYAN_EX
LIGHTMAGENTA_EX = Fore.LIGHTMAGENTA_EX
LIGHTGREEN_EX = Fore.LIGHTGREEN_EX

RESET = Style.RESET_ALL

def colorPrint(*args):
    for text, color in args:
        print(f"{color}{text}{RESET}", end="")
    print()