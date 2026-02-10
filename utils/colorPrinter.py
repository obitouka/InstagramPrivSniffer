"""
InstagramPrivSniffer - Color Printing Utility Module

This module provides color printing capabilities for the InstagramPrivSniffer tool.
It uses Colorama for cross-platform compatibility, especially for Windows terminals.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission
"""

from colorama import init, Fore, Back, Style
import sys
import os

# Initialize colorama on Windows
init(autoreset=True)

# Define colors using colorama
BLACK = Fore.BLACK
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE

# Custom colors using Style.BRIGHT for brighter versions
LIGHT_BLACK_EX = Style.BRIGHT + Fore.BLACK
LIGHT_RED_EX = Style.BRIGHT + Fore.RED
LIGHT_GREEN_EX = Style.BRIGHT + Fore.GREEN
LIGHT_YELLOW_EX = Style.BRIGHT + Fore.YELLOW
LIGHT_BLUE_EX = Style.BRIGHT + Fore.BLUE
LIGHT_MAGENTA_EX = Style.BRIGHT + Fore.MAGENTA
LIGHT_CYAN_EX = Style.BRIGHT + Fore.CYAN

GRAY = LIGHT_BLACK_EX
DARK_GRAY_EX = LIGHT_BLACK_EX

# For orange, we'll use a yellow that looks more orange-like
ORANGE = Fore.LIGHTYELLOW_EX

# Background colors
BG_BLACK = Back.BLACK
BG_RED = Back.RED
BG_GREEN = Back.GREEN
BG_YELLOW = Back.YELLOW
BG_BLUE = Back.BLUE
BG_MAGENTA = Back.MAGENTA
BG_CYAN = Back.CYAN
BG_WHITE = Back.WHITE
BG_LIGHTYELLOW_EX = Back.LIGHTYELLOW_EX

# Text styles
BOLD = Style.BRIGHT
BOLD_OFF = Style.NORMAL
FAINT = Style.DIM
ITALIC = "\033[3m"  # Not supported in all terminals, kept for compatibility
ITALIC_OFF = "\033[23m"
UNDERLINE = "\033[4m"  # Not supported in all terminals, kept for compatibility
BLINK = "\033[6m"  # Not supported in all terminals, kept for compatibility
NEGATIVE = "\033[7m"  # Not supported in all terminals, kept for compatibility
STRIKE = "\033[9m"  # Not supported in all terminals, kept for compatibility

RESET = Style.RESET_ALL


def colorPrint(*args):
    """
    Print colored text by joining multiple color and text arguments.
    
    Args:
        *args: Variable number of color and text arguments to print
        
    This function joins all arguments with the RESET code at the end to ensure
    colors don't bleed into subsequent console output.
    """
    print("".join(str(arg) for arg in args) + RESET)



def customColorPrint(*args):
    """
    Print text in custom RGB colors by mapping to the closest available colorama color.
    
    Args:
        *args: Sequence of (r, g, b, text) values to print in custom colors
        
    Since Colorama doesn't support RGB colors directly, this function maps
    RGB values to the nearest available colorama color using get_closest_color().
    Arguments should be in groups of 4: (r, g, b, text).
    """
    # Since Colorama doesn't support RGB colors directly, we'll use the closest available colors
    i = 0
    while i < len(args):
        r = args[i]
        g = args[i+1]
        b = args[i+2]
        text = args[i+3]
        
        # Convert RGB to the nearest colorama color
        color_code = get_closest_color(r, g, b)
        print(color_code + str(text) + RESET)
        i += 4
    print()


def get_closest_color(r, g, b):
    """
    Map RGB color values to the closest available colorama color.
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
        
    Returns:
        str: Closest colorama color code to the given RGB value
        
    This is a simplified RGB to colorama color mapping that determines
    the closest color based on the relative intensities of RGB components.
    """
    
    if r > g and r > b:
        return Fore.RED if r > 128 else Fore.LIGHTRED_EX
    elif g > r and g > b:
        return Fore.GREEN if g > 128 else Fore.LIGHTGREEN_EX
    elif b > r and b > g:
        return Fore.BLUE if b > 128 else Fore.LIGHTBLUE_EX
    elif r == g == b:
        return Fore.WHITE if r > 128 else Fore.LIGHTBLACK_EX
    else:
        # Mixed colors default to yellow/cyan/magenta based on combinations
        if r > 128 and g > 128:
            return Fore.YELLOW
        elif r > 128 and b > 128:
            return Fore.MAGENTA
        elif g > 128 and b > 128:
            return Fore.CYAN
        else:
            return ''