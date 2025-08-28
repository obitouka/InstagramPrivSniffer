from .base import ProviderPlugin
import requests
import instaloader
import os

class InstagramPlugin(ProviderPlugin):
    def __init__(self):
        self.name = "Instagram"

    def get_posts(self, username, proxies=None):
        """Fetches collaborated posts for a given Instagram username."""
        L = instaloader.Instaloader(download_videos=False, save_metadata=False)
        if proxies:
            L.context.proxies = proxies

        posts_data = []
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            for post in profile.get_posts():
                # We are only interested in collaborated posts for this plugin's purpose
                if post.is_pinned or username not in [p.username for p in post.get_dependencies()]:
                    posts_data.append({
                        "url": f"https://www.instagram.com/p/{post.shortcode}",
                        "caption": post.caption,
                        "likes": post.likes,
                        "comments": post.comments
                    })
            return posts_data
        except Exception as e:
            print(f"An error occurred while fetching posts for {username}: {e}")
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
