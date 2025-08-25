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
        if response.status_code != 200:
            colorPrint(f"Failed: {response.status_code}", RED)
            return

        user_data = response.json()["data"]["user"]

        if user_data.get("is_private"):
            colorPrint("The profile is Private. Fetching only collaborated posts (if available)...", LIGHTYELLOW_EX)
        else:
            colorPrint("The profile is Public. Fetching only collaborated posts (if available)...", LIGHTYELLOW_EX)

        edges = user_data["edge_owner_to_timeline_media"]["edges"]

        if not edges:
            colorPrint("No posts found.", RED)
            return

        for i, edge in enumerate(edges, start=1):
            shortcode = edge["node"]["shortcode"]
            colorPrint(f"{i}: https://www.instagram.com/p/{shortcode}", LIGHTBLUE_EX)

    except Exception as e:
        colorPrint(f"Error: {str(e)}", RED)

#print("WARNING: Only works for media from private/public profiles with collaborations")