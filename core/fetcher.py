"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

import requests

from utils.colorPrinter import *

def getPosts(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "X-IG-App-ID": "936619743392459",
        "Referer": f"https://www.instagram.com/{username}/",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 404 :
            colorPrint((f"[ERROR_CODE] 404", RED))
            colorPrint(("[INFO] Invalid user ID", LIGHTGREEN_EX))
        elif response.status_code == 401 :
            colorPrint((f"[ERROR_CODE] 401", RED))
            colorPrint(("[WARNING] Instagram added rate limit to your IP. Try again later", YELLOW))
        elif response.status_code != 200 :
            colorPrint((f"[ERROR_CODE] {response.status_code}", RED))
            colorPrint(("[ERROR] Something went wrong", RED))

        user_data = response.json()["data"]["user"]

        if user_data.get("is_private"):
            colorPrint(("The profile is Private. Fetching only collaborated posts (if available)...", LIGHTYELLOW_EX))
        else:
            colorPrint(("The profile is Public. Fetching only collaborated posts (if available)...", LIGHTYELLOW_EX))

        edges = user_data["edge_owner_to_timeline_media"]["edges"]

        if not edges:
            colorPrint(("[INFO] ", LIGHTGREEN_EX), ("No posts found", RED))
            return

        for post_item in edges:
            post_data  = post_item["node"]
            post_url  = post_data["shortcode"]
            colorPrint(("[POST]  \t\b", LIGHTCYAN_EX), ("[INFO] ", LIGHTGREEN_EX), (f"https://www.instagram.com/p/{post_url}", LIGHTBLUE_EX))

            for collaborator_item  in post_data["edge_media_to_tagged_user"]["edges"]:
                collaborator_username  = collaborator_item["node"]["user"]["username"]
                colorPrint(("[COLLABORATOR] ", LIGHTCYAN_EX), ("[INFO] ", LIGHTGREEN_EX), (f"https://www.instagram.com/{collaborator_username}", LIGHTBLUE_EX))
            
            print()

    except Exception as e:
        colorPrint((f"\n[ERROR] {str(e)}", RED))

#print("WARNING: Only works for media from private/public profiles with collaborations")