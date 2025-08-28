from .base import ProviderPlugin
import requests
import instaloader
import os

class InstagramPlugin(ProviderPlugin):
    def __init__(self):
        self.name = "Instagram"

    def get_posts(self, username, proxies=None):
        """Fetches collaborated posts for a given Instagram username."""
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "X-IG-App-ID": "936619743392459",
            "Referer": f"https://www.instagram.com/{username}/",
        }

        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            if response.status_code != 200:
                print(f"Failed to fetch data: Status code {response.status_code}")
                return None

            user_data = response.json()["data"]["user"]
            edges = user_data["edge_owner_to_timeline_media"]["edges"]

            if not edges:
                return []

            posts = [f"https://www.instagram.com/p/{edge['node']['shortcode']}" for edge in edges]
            return posts

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")
        except KeyError:
            print("Could not retrieve user data. The profile may not exist or there was an API change.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def get_shortcode_from_url(self, url):
        """Extracts the shortcode from an Instagram post URL."""
        return url.split("/")[-2]

    def download_posts(self, username, post_urls, proxies=None):
        """Downloads media from a list of post URLs."""
        L = instaloader.Instaloader(download_videos=True, download_video_thumbnails=False, save_metadata=False)
        if proxies:
            L.context.proxies = proxies

        if not os.path.exists(username):
            os.makedirs(username)

        L.dirname_pattern = username

        for url in post_urls:
            shortcode = self.get_shortcode_from_url(url)
            try:
                post = instaloader.Post.from_shortcode(L.context, shortcode)
                L.download_post(post, target=username)
            except Exception as e:
                print(f"Could not download post {url}. Reason: {e}")
        print(f"Finished downloading media for {username}.")
