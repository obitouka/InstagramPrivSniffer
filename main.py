"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from core.privMediaFetcher import getPosts
from lib.banner import printBanner
from utils.parser import getArguments

args = getArguments()

if args.name:
    printBanner()
    getPosts(args.name)
'''elif args.version:
    print(f"InstagramPrivSniffer {__version__}")
'''