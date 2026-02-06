"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from curl_cffi import requests
from utils.colorPrinter import *
from datetime import datetime

is_video = None
media_url = None
file_name = None

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def fetch_media(url):
    global is_video, media_url, file_name
    parts = url.split("/")
    
    if len(parts) < 6 or parts[4] not in ("p", "reel"):
        colorPrint(
            CYAN, f"[{get_time()}] \t",
            RED, "[ERROR] \t",
            RED, "Invalid URL format"
        )
        colorPrint(
            CYAN, f"[{get_time()}] \t",
            YELLOW, "[EXAMPLE] \t",
            LIGHT_BLUE_EX, 
            '''https://www.instagram.com/keyloggerluvr/p/V2tgdUTWI6kLka3N/ 
                                                                or 
                                https://www.instagram.com/keyloggerluvr/reel/V2tgdUTWI6kLka3N/\n
            '''
        )
        exit()

    user_name = parts[3]
    shortcode = parts[5]
    file_name = f"{user_name}-{'reel' if parts[4] == 'reel' else 'post'}-{shortcode.replace('-', '')[:10]}{'.mp4' if parts[4] == 'reel' else '.png'}"
    
    colorPrint(
        CYAN, f"[{get_time()}] \t",
        GREEN, "[INFO] \t\t", 
        LIGHT_YELLOW_EX, "Fetching..."
    )
    
    r = requests.get(
        f"https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}",
        headers={
            "X-IG-App-ID": "936619743392459",
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
            CYAN, f"[{get_time()}] \t",
            RED, f"[{r.status_code}] \t\t",
            YELLOW, "[WARNING] \t",
            RED, "Failed to fetch media data"
        )


def download_media(post_url):
    global is_video, media_url, file_name
    fetch_media(post_url)

    if not media_url:
        colorPrint(
            CYAN, f"[{get_time()}] \t",
            RED, "[ERROR] \t",
            RED, "Invalid URL"
        )
        return

    colorPrint(
        CYAN, f"[{get_time()}] \t",
        GREEN, "[INFO] \t\t",
        LIGHT_YELLOW_EX, "Downloading..."
    )

    r = requests.get(
        media_url, 
        headers={
            "X-IG-App-ID": "936619743392459"
        }
    )

    if r.status_code == 200:
        with open(f"InstaDownloads\\{file_name}", "wb") as f:
            f.write(r.content)

        colorPrint(
            CYAN, f"[{get_time()}] \t",
            GREEN, "[SUCCESS] \t",
            LIGHT_YELLOW_EX, "Downloaded ",
            LIGHT_BLUE_EX, ITALIC, f"{file_name} ", ITALIC_OFF,
            LIGHT_YELLOW_EX, f"at {ITALIC}'InstaDownloads'{ITALIC_OFF} folder"
        )
    elif r.status_code == 429:
        colorPrint(
            CYAN, f"[{get_time()}] \t",
            RED, "[429] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Instagram added rate limit to your IP. Try again later"
        )
    else:
        colorPrint(
            CYAN, f"[{get_time()}] \t",
            RED, f"[{r.status_code}] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Failed to download media"
        )
