"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

import requests
from utils.colorPrinter import *

is_video = None
media_url = None

def mediaFetcher(url):
    global is_video, media_url
    parts = url.split("/")
    
    if len(parts) < 6 or parts[4] not in ("p", "reel"):
        colorPrint(("[ERROR] \t", RED), ("Invalid URL format", RED))
        colorPrint(("[EXAMPLE] \t", LIGHTCYAN_EX), ("https://www.instagram.com/p/V2tgdUTWI6kLka3N/ or https://www.instagram.com/reel/V2tgdUTWI6kLka3N/\n", LIGHTBLUE_EX))
        exit()

    username = parts[3]
    shortcode = parts[5]
    
    colorPrint(("Fetching...", LIGHTYELLOW_EX))
    
    r = requests.get(
        f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}",
        headers={
            "X-IG-App-ID": "936619743392459"
        }
    )

    try:
        edges = r.json()["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
        for edge in edges:
            node = edge["node"]
            if node["shortcode"] == shortcode:
                if node["is_video"]:
                    is_video = True
                    media_url = node["video_url"]
                else:
                    is_video = False
                    media_url = node["display_url"]
                break
    except :
        colorPrint((f"[{r.status_code}] \t\t", RED),("[WARNING] \t", YELLOW), (f"Failed to fetch media data", RED))



def downloadMedia(post_url):
    global is_video, media_url
    mediaFetcher(post_url)

    if not media_url:
        colorPrint(("[ERROR] \t", RED), ("Invalid URL", RED))
        return

    colorPrint(("Downloading...", LIGHTYELLOW_EX))

    r = requests.get(
        media_url, 
        headers = {
            "X-IG-App-ID": "936619743392459"
        }
    )

    filename = "video.mp4" if is_video else "image.jpg"

    if r.status_code == 200:
        with open(f"InstaDownloads\{filename}", "wb") as f:
            f.write(r.content)
        colorPrint(("[SUCCESS] \t", LIGHTGREEN_EX), ("Downloaded ", LIGHTYELLOW_EX), (f"{filename} ", LIGHTBLUE_EX), ("at 'InstaDownloads' folder", LIGHTYELLOW_EX))
    else:
        colorPrint((f"[{r.status_code}] \t\t\b", RED),("[WARNING] \t", YELLOW), (f"Failed to download media", RED))
