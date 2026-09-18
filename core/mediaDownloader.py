from curl_cffi import requests
from utils.colorPrinter import *
from datetime import datetime
import os
import re
import html
import json

is_video = None
media_url = None
file_name = None


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def log(label, message, label_color=GREEN, message_color=RED):
    colorPrint(
        CYAN, f"[{get_time()}]  ",
        label_color, f"[{label}]".ljust(15),
        message_color, message
    )


def clean_url(url):
    url = html.unescape(url)
    return (
        url.replace("\\/", "/")
        .replace("\\u0026", "&")
        .replace("\\u003D", "=")
        .replace("\\u002F", "/")
    )


def extract_media(page, shortcode, video=False):
    if video:
        patterns = [
            r'"code"\s*:\s*"' + re.escape(shortcode) + r'".*?"video_versions"\s*:\s*\[.*?"url"\s*:\s*"([^"]+)"',
            r'"code"\s*:\s*"' + re.escape(shortcode) + r'".*?"video_url"\s*:\s*"([^"]+)"',
            r'<meta[^>]+property=["\']og:video["\'][^>]+content=["\']([^"\']+)["\']'
        ]
    else:
        patterns = [
            r'"code"\s*:\s*"' + re.escape(shortcode) + r'".*?"image_versions2"\s*:\s*\{.*?"candidates"\s*:\s*\[.*?"url"\s*:\s*"([^"]+)"',
            r'"code"\s*:\s*"' + re.escape(shortcode) + r'".*?"display_url"\s*:\s*"([^"]+)"',
            r'"code"\s*:\s*"' + re.escape(shortcode) + r'".*?"display_uri"\s*:\s*"([^"]+)"',
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']'
        ]

    for pattern in patterns:
        match = re.search(pattern, page, re.DOTALL | re.IGNORECASE)
        if match:
            return clean_url(match.group(1))

    return None


def fetch_graphql_media(shortcode, post_url):
    try:
        session = requests.Session()

        session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.instagram.com",
            "Referer": post_url
        })

        session.get(
            "https://www.instagram.com/",
            impersonate="chrome",
            timeout=15
        )

        variables = {
            "shortcode": shortcode,
            "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider": False
        }

        response = session.post(
            "https://www.instagram.com/graphql/query",
            data={
                "variables": json.dumps(variables, separators=(",", ":")),
                "doc_id": "27128499623469141",
                "server_timestamps": "true"
            },
            headers={
                "X-CSRFToken": session.cookies.get("csrftoken", "")
            },
            impersonate="chrome",
            timeout=15
        )

        if response.status_code != 200:
            return None

        data = response.json()

        items = (
            data.get("data", {})
            .get("xdt_api__v1__media__shortcode__web_info", {})
            .get("items", [])
        )

        if items:
            versions = items[0].get("video_versions", [])

            if versions:
                return clean_url(versions[0].get("url", ""))

    except Exception:
        pass

    return None


def fetch_media(url, debug=False):
    global is_video, media_url, file_name

    match = re.match(
        r"^https?://(?:www\.)?instagram\.com/([^/]+)/(p|reel|reels)/([^/?#]+)/?$",
        url
    )

    if not match:
        log("ERROR", "Invalid Instagram URL")
        return False

    username, post_type, shortcode = match.groups()

    is_video = post_type in ("reel", "reels")
    file_type = "reel" if is_video else "post"
    extension = ".mp4" if is_video else ".jpg"

    file_name = (
        f"{username}-{file_type}-"
        f"{shortcode.replace('-', '')[:10]}"
        f"{extension}"
    )

    log("INFO", "Fetching media...", GREEN, LIGHT_YELLOW_EX)

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            impersonate="chrome",
            timeout=15
        )

        if response.status_code != 200:
            error_handler(response)
            return False

        if "/accounts/login/" in response.url:
            log("ERROR", "Instagram login required")
            return False

        page = response.text
        media_url = extract_media(page, shortcode, is_video)

        if not media_url and is_video:
            media_url = fetch_graphql_media(shortcode, url)

        if not media_url:
            log("ERROR", "Media URL not found")

            if debug:
                log("DEBUG", f"Final URL: {response.url}", YELLOW, RED)

            return False

        return True

    except requests.exceptions.Timeout:
        log("ERROR", "Request timed out")

    except requests.exceptions.ConnectionError:
        log("ERROR", "Could not connect to Instagram")

    except requests.exceptions.RequestException as e:
        log("ERROR", str(e))

    return False


def error_handler(response):
    log(
        f"ERROR:{response.status_code}",
        "Failed to fetch media"
    )


def download_media(post_url, debug=False):
    global media_url, file_name

    if not fetch_media(post_url, debug):
        return

    log("INFO", "Downloading...", GREEN, LIGHT_YELLOW_EX)

    try:
        response = requests.get(
            media_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": post_url
            },
            impersonate="chrome",
            timeout=30
        )

        if response.status_code != 200:
            log(
                f"ERROR:{response.status_code}",
                "Failed to download media"
            )
            return

        download_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "InstaDownloads"
        )

        os.makedirs(download_path, exist_ok=True)

        file_path = os.path.join(
            download_path,
            file_name
        )

        with open(file_path, "wb") as f:
            f.write(response.content)

        log(
            "SUCCESS",
            f"Downloaded {file_name} at 'InstaDownloads'",
            GREEN,
            LIGHT_YELLOW_EX
        )

    except requests.exceptions.Timeout:
        log("ERROR", "Download timed out")

    except requests.exceptions.ConnectionError:
        log("ERROR", "Could not connect to media server")

    except requests.exceptions.RequestException as e:
        log("ERROR", str(e))