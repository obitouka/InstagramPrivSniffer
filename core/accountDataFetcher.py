"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""

from curl_cffi import requests
from utils.colorPrinter import *
from datetime import datetime
import re


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def log(label, message, label_color=GREEN, message_color=RED):
    colorPrint(
        CYAN, f"[{get_time()}]  ",
        label_color, f"[{label}]".ljust(15),
        message_color, message
    )


def fetch_data(username, debug=False):
    log("INFO", "Fetching posts...", GREEN, LIGHT_YELLOW_EX)

    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            impersonate="chrome",
            timeout=15
        )

        if response.status_code != 200:
            error_handler(response, debug)
            return

        page = response.text
        result = check_page(page, username, response.url)

        if result != "valid":
            error_handler(response, debug, result, page, username)
            return

        account_type(page)
        get_posts(page)

    except requests.exceptions.Timeout:
        log("ERROR", "Request timed out")
    except requests.exceptions.ConnectionError:
        log("ERROR", "Could not connect to Instagram")
    except requests.exceptions.RequestException as e:
        log("ERROR", str(e))
    except Exception as e:
        log("ERROR", str(e))


def check_page(page, username, final_url):
    if re.search(r'"is_private"\s*:\s*(true|false)', page):
        return "valid"

    if "/accounts/login/" in final_url:
        return "login"

    if ("challenge_required" in page or "checkpoint_required" in page or "/challenge/" in final_url or "/checkpoint/" in final_url):
        return "challenge"

    if "login_required" in page:
        return "login"

    if ("rate_limit" in page or "too many requests" in page.lower() or "please wait a few minutes before you try again" in page.lower()):
        return "rate_limit"

    return "unknown"


def error_handler(response, debug=False, error_type=None, page="", username=""):
    if error_type == "challenge":
        message = "Instagram challenge or checkpoint required"
    elif error_type == "login":
        message = "Instagram login required to view this profile"
    elif error_type == "rate_limit":
        message = "Instagram rate limited your IP"
    elif error_type == "unknown":
        message = "User not found"
    elif response.status_code == 400:
        message = "Bad request"
    elif response.status_code == 401:
        message = "Instagram rejected the request"
    elif response.status_code == 403:
        message = "Access denied by Instagram"
    elif response.status_code == 404:
        message = "User not found"
    elif response.status_code == 429:
        message = "Instagram rate limited your IP"
    elif response.status_code >= 500:
        message = "Instagram server error"
    else:
        message = "Unexpected response from Instagram"

    if response.status_code == 429 or error_type == "rate_limit":
        log(
            f"WARNING:{response.status_code}",
            message,
            YELLOW,
            RED
        )
    else:
        log(
            f"ERROR:{response.status_code}",
            message,
            RED,
            RED
        )

    if not debug:
        return

    username_found = bool(
        re.search(
            r'"username"\s*:\s*"' + re.escape(username) + r'"',
            page
        )
    )

    private_found = bool(
        re.search(
            r'"is_private"\s*:\s*(true|false)',
            page
        )
    )

    post_count = len(
        re.findall(
            r'"__isXIGPolarisMedia"\s*:\s*"XIGPolaris(?:Image|Video)Media"',
            page
        )
    )

    challenge_found = (
        "challenge_required" in page
        or "checkpoint_required" in page
        or "/challenge/" in response.url
        or "/checkpoint/" in response.url
    )

    login_found = (
        "login_required" in page
        or "/accounts/login/" in response.url
    )

    rate_limit_found = (
        "rate_limit" in page
        or "too many requests" in page.lower()
        or "please wait a few minutes before you try again" in page.lower()
    )

    title = re.search(
        r"<title[^>]*>(.*?)</title>",
        page,
        re.IGNORECASE | re.DOTALL
    )

    if title:
        title = re.sub(r"\s+", " ", title.group(1)).strip()
    else:
        title = "Not found"

    log("DEBUG", "Request diagnostics", YELLOW, RED)

    debug_data = [
        ("HTTP status", response.status_code),
        ("Final URL", response.url),
        ("Content type", response.headers.get("content-type", "Unknown")),
        ("Response size", f"{len(page)} bytes"),
        ("Page title", title),
        ("Username marker", "FOUND" if username_found else "NOT FOUND"),
        ("Profile marker", "FOUND" if private_found else "NOT FOUND"),
        ("Post objects", post_count),
        ("Login redirect", "FOUND" if login_found else "NOT FOUND"),
        ("Challenge", "FOUND" if challenge_found else "NOT FOUND"),
        ("Rate limit", "FOUND" if rate_limit_found else "NOT FOUND"),
        ("Result", error_type or "HTTP error")
    ]

    for name, value in debug_data:
        colorPrint(RED, f"{name:<17}: {value}")


def account_type(page):
    match = re.search(
        r'"is_private"\s*:\s*(true|false)',
        page
    )

    if not match:
        return

    account = "Private profile" if match.group(1) == "true" else "Public profile"
    log("TYPE", account, GREEN, RED)


def get_posts(page):
    pattern = re.compile(
        r'"__isXIGPolarisMedia"\s*:\s*"XIGPolaris(?:Image|Video)Media".*?'
        r'"code"\s*:\s*"([^"]+)".*?'
        r'"media_type"\s*:\s*(\d+).*?'
        r'"user"\s*:\s*\{.*?'
        r'"username"\s*:\s*"([^"]+)"',
        re.DOTALL
    )

    posts = pattern.findall(page)

    if not posts:
        log("POST", "No posts found", GREEN, RED)
        return

    seen = set()
    count = 0

    for code, media_type, owner in posts:
        if code in seen:
            continue

        seen.add(code)
        count += 1

        colorPrint(
            YELLOW,
            f"+--------------------------------------------------------[{count}]-------------------------------------------------------+\n"
        )

        if media_type == "2":
            log(
                "VIDEO",
                f"https://www.instagram.com/{owner}/reel/{code}",
                GREEN,
                LIGHT_BLUE_EX
            )
        else:
            log(
                "IMAGE",
                f"https://www.instagram.com/{owner}/p/{code}",
                GREEN,
                LIGHT_BLUE_EX
            )

        print()