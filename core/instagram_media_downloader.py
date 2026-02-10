"""
InstagramPrivSniffer - Instagram Media Downloader Module

This module handles downloading media from Instagram posts using post URLs or post numbers.
Provides functionality for fetching and downloading both individual posts and bulk downloads.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission
"""

from curl_cffi import requests
from utils.colorPrinter import *
from datetime import datetime

# Global variables to store media information
is_video = None
media_url = None
file_name = None


def make_api_request(username):
    """
    Make an API request to fetch Instagram user data.
    
    Args:
        username (str): Instagram username to fetch data for
        
    Returns:
        Response object from the API request or None if error occurred
    """
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "X-IG-App-ID": "936619743392459",
    }
    try:
        response = requests.get(url, headers=headers)
        return response
    except Exception as e:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[ERROR] \t\t\b",
            RED, f"Request failed: {str(e)}"
        )
        return None


def download_instagram_media_by_number(username, post_number):
    """
    Download Instagram media by post number (0 for all, 1-n for specific post).
    
    Args:
        username (str): Instagram username to fetch posts from
        post_number (int): Post number to download (0 for all, 1-n for specific post)
        
    Fetches the user's posts and downloads the specified post(s) based on the post_number:
    - post_number = 0: Downloads all posts from the user
    - post_number = N (where N > 0): Downloads the Nth post from the user
    """
    colorPrint(
        CYAN, f"[{get_current_time()}] \t",
        GREEN, "[INFO] \t\t", 
        LIGHT_YELLOW_EX, f"Fetching user {username}'s posts..."
    )
    
    response = make_api_request(username)
    
    if response and response.status_code != 200:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, f"[{response.status_code}] \t\t\b",
            RED, "[ERROR] \t\t",
            RED, "Failed to fetch user data"
        )
        return
    
    try:
        user_data = response.json()["data"]["user"]
        edges = user_data["edge_owner_to_timeline_media"]["edges"]
        
        if not edges:
            colorPrint(
                CYAN, f"[{get_current_time()}] \t",
                RED, "[ERROR] \t\t",
                RED, "No posts found for this user"
            )
            return
        
        total_posts = len(edges)
        
        if post_number == 0:
            # Download all posts
            colorPrint(
                CYAN, f"[{get_current_time()}] \t",
                GREEN, "[INFO] \t\t",
                LIGHT_YELLOW_EX, f"Downloading all {total_posts} posts..."
            )
            for i, post_item in enumerate(edges, 1):
                download_single_post(post_item, i, total_posts)
        elif 1 <= post_number <= total_posts:
            # Download specific post
            post_item = edges[post_number - 1]  # Convert to 0-based index
            download_single_post(post_item, post_number, total_posts)
        else:
            colorPrint(
                CYAN, f"[{get_current_time()}] \t",
                RED, "[ERROR] \t\t",
                RED, f"Post number {post_number} is out of range. User has {total_posts} posts."
            )
            
    except Exception as e:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[ERROR] \t\t",
            RED, f"Failed to download media: {str(e)}"
        )


def download_single_post(post_item, post_index, total_posts):
    """
    Download a single Instagram post.
    
    Args:
        post_item (dict): Dictionary containing post data from Instagram API
        post_index (int): Index of the current post (for display purposes)
        total_posts (int): Total number of posts (for display purposes)
        
    Downloads the media (image or video) from a single post item
    and saves it to the InstaDownloads folder with an appropriate filename.
    """
    post_data = post_item["node"]
    shortcode = post_data["shortcode"]
    is_video = post_data["is_video"]
    media_url = post_data["video_url"] if is_video else post_data["display_url"]
    owner_username = post_data["owner"]["username"]
    
    file_name = f"{owner_username}-{'reel' if is_video else 'post'}-{shortcode.replace('-', '')[:10]}{'.mp4' if is_video else '.png'}"
    
    download_media_from_url(media_url, file_name, post_index, total_posts)


def download_media_from_url(media_url, file_name, post_index=None, total_posts=None):
    """
    Download media from a given URL and save to file.
    
    Args:
        media_url (str): URL of the media to download
        file_name (str): Name to save the file as
        post_index (int, optional): Index of current post for display
        total_posts (int, optional): Total posts for display
    """
    if post_index is not None and total_posts is not None:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            GREEN, "[INFO] \t\t",
            LIGHT_YELLOW_EX, f"Downloading post {post_index}/{total_posts}: {file_name}..."
        )
    else:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
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
            CYAN, f"[{get_current_time()}] \t",
            GREEN, "[SUCCESS] \t",
            LIGHT_YELLOW_EX, "Downloaded ",
            LIGHT_BLUE_EX, f"{file_name} ",
            LIGHT_YELLOW_EX, f"at 'InstaDownloads' folder"
        )
    elif r.status_code == 429:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[429] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Instagram added rate limit to your IP. Try again later"
        )
    else:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, f"[{r.status_code}] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Failed to download media"
        )


def get_current_time():
    """
    Get current time in HH:MM:SS format.
    
    Returns:
        str: Current time formatted as HH:MM:SS
    """
    return datetime.now().strftime("%H:%M:%S")


def fetch_media_from_url(url):
    """
    Fetch media information from an Instagram URL.
    
    Args:
        url (str): Instagram post URL to fetch media from
        
    This function extracts the username and shortcode from the URL,
    fetches the media data from Instagram's API, and sets global variables
    with the media information.
    """
    global is_video, media_url, file_name
    parts = url.split("/")
    
    if len(parts) < 6 or parts[4] not in ("p", "reel"):
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[ERROR] \t",
            RED, "Invalid URL format"
        )
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
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
        CYAN, f"[{get_current_time()}] \t",
        GREEN, "[INFO] \t\t", 
        LIGHT_YELLOW_EX, "Fetching..."
    )
    
    r = make_api_request(user_name)
    
    if not r:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[ERROR] \t",
            RED, "Failed to make API request"
        )
        return

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
            CYAN, f"[{get_current_time()}] \t",
            RED, f"[{r.status_code}] \t\t",
            YELLOW, "[WARNING] \t",
            RED, "Failed to fetch media data"
        )


def download_instagram_media(post_url):
    """
    Download Instagram media from a given URL.
    
    Args:
        post_url (str): Instagram post URL to download media from
        
    Downloads the media (image or video) from the provided Instagram URL
    and saves it to the InstaDownloads folder with an appropriate filename.
    """
    global is_video, media_url, file_name
    fetch_media_from_url(post_url)

    if not media_url:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[ERROR] \t",
            RED, "Invalid URL"
        )
        return

    download_media_from_url(media_url, file_name)