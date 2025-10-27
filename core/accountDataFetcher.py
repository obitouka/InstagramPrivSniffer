"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

import requests
from utils.colorPrinter import *


def fetch_data(username):
    colorPrint(LIGHT_YELLOW_EX, "Fetching only collaborated posts (if available)...")
    
    try:
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "X-IG-App-ID": "936619743392459",
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            error_handler(response)
            return 

        user_data = response.json()["data"]["user"]
        
        account_type(user_data)
        get_posts(user_data)
        
    except Exception as e:
        colorPrint(
            RED, f"[{response.status_code}] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Failed to fetch account data"
        )


def error_handler(response):
    if response.status_code == 404:
        colorPrint(
            RED, "[404] \t\t\b",
            RED, "[ERROR] \t\t",
            RED, "User not found"
        )
    elif response.status_code == 401:
        colorPrint(
            RED, "[401] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Instagram added rate limit to your IP. Try again later"
        )
    else:
        colorPrint(
            RED, f"[{response.status_code}] \t\t\b",
            RED, "[ERROR] \t\t",
            RED, "Something went wrong"
        )


def account_type(user_data):
    if user_data.get("is_private"):
        colorPrint(
            CYAN, "[TYPE]  \t\b",
            GREEN, "[INFO] \t",
            RED, "Private profile\n"
        )
    else:
        colorPrint(
            CYAN, "[TYPE]  \t\b",
            GREEN, "[INFO] \t",
            RED, "Public profile\n"
        )


def get_posts(user_data):
    edges = user_data["edge_owner_to_timeline_media"]["edges"]

    if not edges:
        colorPrint(
            CYAN, "[POST]  \t\b",
            GREEN, "[INFO] \t",
            RED, "No posts found"
        )
    else:
        for i, post_item in enumerate(edges, 1):
            post_data = post_item["node"]
            post_url = post_data["shortcode"]
            is_video = post_data["is_video"]
            post_owner = post_data["owner"]["username"]

            colorPrint(YELLOW, f"+----------------------------------------------------[{i}]----------------------------------------------------+\n")

            if is_video:
                colorPrint(
                    CYAN, "[VIDEO]  \t\b",
                    GREEN, "[INFO] \t",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}/reel/{post_url}"
                )
            else:
                colorPrint(
                    CYAN, "[IMAGE]  \t\b",
                    GREEN, "[INFO] \t",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}/p/{post_url}"
                )

            colorPrint(
                CYAN, "[OWNER] \t\b",
                GREEN, "[INFO] \t",
                LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}"
            )

            for collaborator_item in post_data["edge_media_to_tagged_user"]["edges"]:
                collaborator_username = collaborator_item["node"]["user"]["username"]
                colorPrint(
                    CYAN, "[COLLABORATOR] ",
                    GREEN, "[INFO] \t",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{collaborator_username}"
                )
            
            print()
