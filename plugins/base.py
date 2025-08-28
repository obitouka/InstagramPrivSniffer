class ProviderPlugin:
    """
    Base class for all provider plugins.
    A provider plugin represents a social media platform or other source of media.
    """
    def __init__(self):
        self.name = "Base Provider"

    def get_posts(self, username, proxies=None):
        """
        Fetches a list of post URLs for a given username.
        Should return a list of strings (URLs).
        """
        raise NotImplementedError

    def download_posts(self, username, post_urls, proxies=None):
        """
        Downloads the media for a list of post URLs.
        """
        raise NotImplementedError
