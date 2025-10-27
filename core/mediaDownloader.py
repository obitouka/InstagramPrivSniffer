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
        colorPrint(
            RED, "[ERROR] \t",
            RED, "Invalid URL format"
        )
        colorPrint(
            YELLOW, "[EXAMPLE] \t",
            LIGHT_BLUE_EX, 
            '''https://www.instagram.com/keyloggerluvr/p/V2tgdUTWI6kLka3N/ 
                                            or 
                https://www.instagram.com/keyloggerluvr/reel/V2tgdUTWI6kLka3N/\n
            '''
        )
        exit()

    username = parts[3]
    shortcode = parts[5]
    
    colorPrint(GREEN, "[INFO] \t\t", LIGHT_YELLOW_EX, "Fetching...")
    
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
    except:
        colorPrint(
            RED, f"[{r.status_code}] \t\t",
            YELLOW, "[WARNING] \t",
            RED, "Failed to fetch media data"
        )


def downloadMedia(post_url):
    global is_video, media_url
    mediaFetcher(post_url)

    if not media_url:
        colorPrint(
            RED, "[ERROR] \t",
            RED, "Invalid URL"
        )
        return

    colorPrint(GREEN, "[INFO] \t\t",LIGHT_YELLOW_EX, "Downloading...")

    r = requests.get(
        media_url, 
        headers={
            "X-IG-App-ID": "936619743392459"
        }
    )

    filename = "video.mp4" if is_video else "image.jpg"

    if r.status_code == 200:
        with open(f"InstaDownloads\\{filename}", "wb") as f:
            f.write(r.content)

        colorPrint(
            GREEN, "[SUCCESS] \t",
            LIGHT_YELLOW_EX, "Downloaded ",
            LIGHT_BLUE_EX, ITALIC, f"{filename} ", ITALIC_OFF,
            LIGHT_YELLOW_EX, f"at {ITALIC}'InstaDownloads'{ITALIC_OFF} folder"
        )
    else:
        colorPrint(
            RED, f"[{r.status_code}] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Failed to download media"
        )
