"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission 
"""

from argparse import ArgumentParser
from lib.version import __version__

def getArguments(): 
    parser = ArgumentParser(
            prog='InstagramPrivSniffer ',
            description="What my tool does: ",
            epilog='Thanks for using my tool!'
        )

    parser.add_argument(
        "-n", "--name", 
        metavar="USERNAME",
        help="Enter username to fetch collaborated posts even from private accounts", 
        type=str
    )

    parser.add_argument(
        "-d", "--download",
        metavar="POST_URL",
        help="Enter post URL to download media", 
        type=str
    )

    parser.add_argument(
        "--version", 
        help="version of this tool", 
        action="version", 
        version=f"InstagramPrviSniffer {__version__}"
    )

    return parser.parse_args()