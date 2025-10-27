"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

BLACK = "\033[0;30m"
RED = "\033[38;2;255;0;0m"
GREEN = "\033[38;2;0;255;0m"
YELLOW = "\033[38;2;255;242;0m"
BLUE = "\033[38;2;33;33;255m"
MAGENTA = "\033[38;2;234;63;247m"
CYAN = "\033[38;2;0;236;255m"
ORANGE = "\033[38;2;255;165;0m"


LIGHT_BLUE_EX = "\033[1;34m"
LIGHT_YELLOW_EX = "\033[1;33m"
GRAY = "\033[0;37m"
DARK_GRAY_EX = "\033[1;30m"


BG_BLACK   = "\033[40m"
BG_RED     = "\033[41m"
BG_GREEN   = "\033[42m"
BG_YELLOW  = "\033[43m"
BG_BLUE    = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN    = "\033[46m"
BG_WHITE   = "\033[47m"
BG_ORANGE = "\033[48;2;255;165;0m" 


BOLD = "\033[1m"
BOLD_OFF = "\033[22m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
ITALIC_OFF = "\033[23m"
UNDERLINE = "\033[4m"
BLINK = "\033[6m"
NEGATIVE = "\033[7m"
STRIKE = "\033[9m"


RESET = "\033[0m"


def colorPrint(*args):
    print("".join(args) + RESET)



def customColorPrint(*args):
    i = 0
    while i < len(args):
        r = args[i]
        g = args[i+1]
        b = args[i+2]
        text = args[i+3]
        print(f"\033[38;2;{r};{g};{b}m{text}{RESET}")
        i += 4
    print()