"""
InstagramPrivSniffer - Instagram Account Data Fetcher Module

This module handles fetching account information and collaborated posts from Instagram.
Provides functionality to display account type and posts for a given username.

Copyright (c) 2026 obitouka
See the file 'LICENSE' for copying permission
"""

from curl_cffi import requests
from utils.colorPrinter import *
from datetime import datetime


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


def get_current_time():
    """
    Get current time in HH:MM:SS format.
    
    Returns:
        str: Current time formatted as HH:MM:SS
    """
    return datetime.now().strftime("%H:%M:%S")


def fetch_instagram_account_data(username):
    """
    Fetch data for an Instagram account, focusing on collaborative posts.
    
    Args:
        username (str): Instagram username to fetch data for
        
    Fetches account data from Instagram's API and displays account information
    including account type (private/public) and collaborated posts.
    """
    colorPrint(
        CYAN, f"[{get_current_time()}] \t",
        GREEN, "[INFO] \t\t\b", 
        LIGHT_YELLOW_EX, "Fetching only collaborated posts (if available)..."
    )
    
    response = make_api_request(username)
    
    if response and response.status_code == 200:
        try:
            user_data = response.json()["data"]["user"]
            
            print_account_type(user_data)
            print_account_posts(user_data)
            
        except Exception as e:
            colorPrint(
                CYAN, f"[{get_current_time()}] \t",
                RED, f"[{response.status_code}] \t\t\b",
                YELLOW, "[WARNING] \t",
                RED, "Failed to fetch account data"
            )
    else:
        handle_api_error(response)
        return


def handle_api_error(response):
    """
    Handle different API error responses from Instagram.
    
    Args:
        response: HTTP response object from the API request
        
    Displays appropriate error messages based on the HTTP status code
    received from Instagram's API.
    """
    if response.status_code == 404:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[404] \t\t\b",
            RED, "[ERROR] \t\t",
            RED, "User not found"
        )
    elif response.status_code == 429:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, "[429] \t\t\b",
            YELLOW, "[WARNING] \t",
            RED, "Instagram added rate limit to your IP. Try again later"
        )
    else:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            RED, f"[{response.status_code}] \t\t\b",
            RED, "[ERROR] \t\t",
            RED, "Something went wrong"
        )


def print_account_type(user_data):
    """
    Print whether the account is private or public.
    
    Args:
        user_data (dict): Dictionary containing user account data from Instagram API
        
    Displays account type information (private or public) to the console.
    """
    if user_data.get("is_private"):
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            GREEN, "[TYPE]  \t\b",
            RED, "Private profile\n"
        )
    else:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            GREEN, "[TYPE]  \t\b",
            RED, "Public profile\n"
        )


def print_account_posts(user_data):
    """
    Print account posts and collaborations.
    
    Args:
        user_data (dict): Dictionary containing user account data from Instagram API
        
    Displays all posts from the user including post URLs, owner information,
    and any collaborators tagged in the posts.
    """
    edges = user_data["edge_owner_to_timeline_media"]["edges"]

    if not edges:
        colorPrint(
            CYAN, f"[{get_current_time()}] \t",
            GREEN, "[POST]  \t\b",
            RED, "No posts found"
        )
    else:
        for i, post_item in enumerate(edges, 1):
            post_data = post_item["node"]
            post_url = post_data["shortcode"]
            is_video = post_data["is_video"]
            post_owner = post_data["owner"]["username"]

            colorPrint(YELLOW, f"+--------------------------------------------------------[{i}]-------------------------------------------------------+\n")

            if is_video:
                colorPrint(
                    CYAN, f"[{get_current_time()}] \t",
                    GREEN, "[VIDEO]  \t\b",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}/reel/{post_url}"
                )
            else:
                colorPrint(
                    CYAN, f"[{get_current_time()}] \t",
                    GREEN, "[IMAGE]  \t\b",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}/p/{post_url}"
                )

            colorPrint(
                CYAN, f"[{get_current_time()}] \t",
                GREEN, "[OWNER] \t\b",
                LIGHT_BLUE_EX, f"https://www.instagram.com/{post_owner}"
            )

            for collaborator_item in post_data["edge_media_to_tagged_user"]["edges"]:
                collaborator_username = collaborator_item["node"]["user"]["username"]
                colorPrint(
                    CYAN, f"[{get_current_time()}] \t",
                    GREEN, "[COLLAB] \t\b",
                    LIGHT_BLUE_EX, f"https://www.instagram.com/{collaborator_username}"
                )
            
            print()