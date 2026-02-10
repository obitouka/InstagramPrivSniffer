"""
InstagramPrivSniffer - Banner Display Module

This module provides the ASCII art banner for the InstagramPrivSniffer tool.
Displays the tool's branding and version information in a stylized format.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission
"""

from lib.version import __version__
from utils.colorPrinter import *

logoCOLOR = GREEN
instagramCOLOR = MAGENTA
privSnifferCOLOR = RED

ver = CYAN + BOLD + __version__ + BOLD_OFF + CYAN + privSnifferCOLOR
name = ORANGE
m = RED + "@" + logoCOLOR  # magnify symbol
d = RED + "X" + logoCOLOR  # dot symbol

logo = fr"""{logoCOLOR}
1010101010101010101010101
1 --------------------- 1
0 ||  0101010101010  || 0	{instagramCOLOR} ___ _   _ ____ _____   _     ____ ____      _    __  __                        {logoCOLOR}    
1 ||  1010101010{d}10  || 1	{instagramCOLOR}|_ _| \ | / ___|_   _| / \   / ___|  _  \   / \  |  \/  |        {name}{"{O}"}{logoCOLOR}
0 ||  01010***10101  || 0	{instagramCOLOR} | ||  \| \___ \ | |  / _ \ | |  _| |_) |  / _ \ | |\/| |        {name}{"{B}"}{logoCOLOR}
1 ||  101*=====*101  || 1	{instagramCOLOR} | || |\  |___) || | / ___ \| |_| |  _ <  / ___ \| |  | |        {name}{"{I}"}{logoCOLOR}
0 ||  010*=====*101  || 0	{instagramCOLOR}|___|_| \_|____/ |_|/_/ {RED}__{MAGENTA}\_\\____|_| \_\/_/ {RED}__{MAGENTA}\_\_|  |_|        {name}{"{T}"}{logoCOLOR}
1 ||  1010*===*1010  || 1	{privSnifferCOLOR}|  _ \ _ __(_)_   _    / ___|_ __  (_) / _| / _| ___  _ __       {name}{"{O}"}{logoCOLOR}
0 ||  01*=====*     *|| 0	{privSnifferCOLOR}| |_) | '__| \ \ / /   \___ \ '_ \ | || |_ | |_ / _ \| '__|      {name}{"{U}"}{logoCOLOR}
1 ||  1*======   {m}   || 1	{privSnifferCOLOR}|  __/| |  | |\ V /     ___) | | | | ||  _||  _|  __/| |         {name}{"{K}"}{logoCOLOR}
0 ||  *=======*     *|| 0	{privSnifferCOLOR}|_|   |_|  |_| \_/{ver}|____/|_| |_|_||_|  |_|  \___||_|         {name}{"{A}"}{logoCOLOR}
1 ||  *===========*  *| 1
0 ------------------*  01
1010101010101010101010101
"""

# Change "=" color to your desired color
logo = logo.replace("=", f"{RED}={logoCOLOR}")

logo = logo.replace("*", f"{DARK_GRAY_EX}*{logoCOLOR}")

def printBanner():
    """
    Print the InstagramPrivSniffer ASCII art banner to the console.
    
    This function displays the tool's branding with colors and formatting.
    If there are any issues with displaying the formatted banner, it falls back
    to displaying the banner without formatting.
    """
    try:
        colorPrint(BOLD, logo, RESET)
    except:
        colorPrint(logo, RESET)
