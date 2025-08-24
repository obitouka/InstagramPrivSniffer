"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from core.fetcher import get_posts
from lib.banner import print_banner
from utils.parser import getArguments

args = getArguments()

if args.name:
    print_banner()
    get_posts(args.name)
'''elif args.version:
    print(f"InstagramPrivSniffer {__version__}")
'''