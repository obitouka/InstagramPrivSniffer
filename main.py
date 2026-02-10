"""
InstagramPrivSniffer - Instagram Media Sniffer Tool

Main entry point for the InstagramPrivSniffer application.
Handles command-line argument parsing and routes to appropriate functionality.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission
"""

from core.instagram_account_fetcher import fetch_instagram_account_data
from core.instagram_media_downloader import download_instagram_media, download_instagram_media_by_number
from lib.banner import printBanner
from utils.colorPrinter import colorPrint, RED
from utils.argument_parser import parse_command_line_arguments

args = parse_command_line_arguments()

if args.name:
    # Fetch and display account information and collaborated posts
    printBanner()
    fetch_instagram_account_data(args.name)
elif args.dload:
    # Handle media download based on argument type (URL or post number)
    printBanner()
    # Check if the argument is a number or a URL
    try:
        post_number = int(args.dload)
        # If it's a number, we need to get the username from the -n flag
        if hasattr(args, 'name') and args.name:
            download_instagram_media_by_number(args.name, post_number)
        else:
            colorPrint(
                RED, "[ERROR] \t\t",
                RED, "Username (-n) is required when using post number with -d flag"
            )
    except ValueError:
        # If it's not a number, treat it as a URL
        download_instagram_media(args.dload)