"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from lib.version import __version__
from utils.colorPrinter import *

logoCOLOR = GREEN
instagramCOLOR = LIGHTMAGENTA_EX
privSnifferCOLOR = RED

ver = LIGHTCYAN_EX + __version__ + privSnifferCOLOR

s = RED + "@" + logoCOLOR

logo = fr"""{logoCOLOR}
1010101010101010101010101
1 --------------------- 1
0 ||  0101010101010  || 0	{instagramCOLOR} ___ _   _ ____ _____   _     ____ ____      _    __  __                        {logoCOLOR}    
1 ||  1010101010 10  || 1	{instagramCOLOR}|_ _| \ | / ___|_   _| / \   / ___|  _ \    / \  |  \/  |        {YELLOW}{"{O}"}{logoCOLOR}
0 ||  01010***10101  || 0	{instagramCOLOR} | ||  \| \___ \ | |  / _ \ | |  _| |_) |  / _ \ | |\/| |        {YELLOW}{"{B}"}{logoCOLOR}
1 ||  101*=====*101  || 1	{instagramCOLOR} | || |\  |___) || | / ___ \| |_| |  _ <  / ___ \| |  | |        {YELLOW}{"{I}"}{logoCOLOR}
0 ||  010*=====*101  || 0	{instagramCOLOR}|___|_| \_|____/ |_|/_/ __\_\\____|_| \_\/_/ __\_\_|  |_|        {YELLOW}{"{T}"}{logoCOLOR}
1 ||  1010*===*1010  || 1	{privSnifferCOLOR}|  _ \ _ __(_)_   _    / ___|_ __  (_) / _| / _| ___  _ __       {YELLOW}{"{O}"}{logoCOLOR}
0 ||  01*=====*     *|| 0	{privSnifferCOLOR}| |_) | '__| \ \ / /   \___ \ '_ \ | || |_ | |_ / _ \| '__|      {YELLOW}{"{U}"}{logoCOLOR}
1 ||  1*======   {s}   || 1	{privSnifferCOLOR}|  __/| |  | |\ V /     ___) | | | | ||  _||  _|  __/| |         {YELLOW}{"{K}"}{logoCOLOR}
0 ||  *=======*     *|| 0	{privSnifferCOLOR}|_|   |_|  |_| \_/{ver}|____/|_| |_|_||_|  |_|  \___||_|         {YELLOW}{"{A}"}{logoCOLOR}
1 ||  *===========*  *| 1
0 ------------------*  01
1010101010101010101010101
"""

# Change "=" color to your desired color
logo = logo.replace("=", f"{RED}={logoCOLOR}")

logo = logo.replace("*", f"{LIGHTBLACK_EX}*{logoCOLOR}")

def printBanner():
    colorPrint((logo, RESET))
