"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from core.accountDataFetcher import fetch_data 
from core.mediaDownloader import downloadMedia
from lib.banner import printBanner
from utils.parser import getArguments

args = getArguments()

if args.name:
    printBanner()
    fetch_data(args.name)
elif args.download:
    printBanner()
    downloadMedia(args.download)