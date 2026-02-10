"""
InstagramPrivSniffer - Command Line Argument Parser Module

This module handles command-line argument parsing for the InstagramPrivSniffer tool.
It defines the available command-line options and their behavior.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission 
"""

from argparse import ArgumentParser
from lib.version import __version__


def parse_command_line_arguments(): 
    """
    Parse and return command line arguments for the InstagramPrivSniffer tool.
    
    Returns:
        argparse.Namespace: Object containing parsed command-line arguments
        
    The function sets up the following arguments:
    - -n/--name: Username to fetch collaborated posts
    - -d/--dload: Post URL or post number to download
    - --version: Show tool version
    """
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
        "-d", "--dload",
        metavar="POSTURL or POSTNUMBER",
        help="Enter post URL to download media or post number (0 for all, 1-n for specific post)", 
        type=str
    )

    parser.add_argument(
        "--version", 
        help="version of this tool", 
        action="version", 
        version=f"InstagramPrivSniffer {__version__}"
    )

    return parser.parse_args()