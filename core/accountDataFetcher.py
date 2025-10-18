"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

import requests
from utils.colorPrinter import *

def fetch_data(username):
    colorPrint(("Fetching only collaborated posts (if available)...", LIGHTYELLOW_EX))
    
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
        colorPrint((f"[{response.status_code}] \t\t\b", RED),("[WARNING] \t", YELLOW), (f"Failed to fetch account data", RED))


def error_handler(response):
    if response.status_code == 404 :
        colorPrint(("[404] \t\t\b", RED), ("[ERROR] \t\t", RED), ("User not found", RED))
    elif response.status_code == 401 :
        colorPrint(("[401] \t\t\b", RED), ("[WARNING] \t", YELLOW), ("Instagram added rate limit to your IP. Try again later", RED))
    else :
        colorPrint((f"[{response.status_code}] \t\t\b", RED), ("[ERROR] \t\t", RED), ("Something went wrong", RED))


def account_type(user_data):
    if user_data.get("is_private"):
        colorPrint(("[TYPE]  \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), ("Private profile\n", RED))
    else:
        colorPrint(("[TYPE]  \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), ("Public profile\n", RED))


def get_posts(user_data):
    edges = user_data["edge_owner_to_timeline_media"]["edges"]
    if not edges:
        colorPrint(("[POST]  \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), ("No posts found", RED))
    else: 
        for post_item in edges:
            post_data  = post_item["node"]
            post_url  = post_data["shortcode"]
            is_video = post_data["is_video"]
            post_owner  = post_data["owner"]["username"]

            if is_video:
                colorPrint(("[VIDEO]  \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), (f"https://www.instagram.com/{post_owner}/reel/{post_url}", LIGHTBLUE_EX))
            else:
                colorPrint(("[IMAGE]  \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), (f"https://www.instagram.com/{post_owner}/p/{post_url}", LIGHTBLUE_EX))

            colorPrint(("[OWNER] \t\b", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), (f"https://www.instagram.com/{post_owner}", LIGHTBLUE_EX))

            for collaborator_item  in post_data["edge_media_to_tagged_user"]["edges"]:
                collaborator_username  = collaborator_item["node"]["user"]["username"]
                colorPrint(("[COLLABORATOR] ", LIGHTCYAN_EX), ("[INFO] \t", LIGHTGREEN_EX), (f"https://www.instagram.com/{collaborator_username}", LIGHTBLUE_EX))
            
            print()