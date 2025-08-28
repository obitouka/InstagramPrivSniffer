import configparser

def load_config():
    """Loads proxy settings from config.ini."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    proxy = config.get('Settings', 'proxy', fallback=None)
    if proxy:
        return {'http': proxy, 'https': proxy}
    return None

def save_posts_to_file(username, posts):
    """Saves a list of posts to a file named after the username."""
    if not posts:
        return

    filename = f"{username}_posts.txt"
    with open(filename, "w") as f:
        for i, post_url in enumerate(posts):
            f.write(f"{i+1}: {post_url}\n")
    print(f"Saved {len(posts)} posts to {filename}")

def main():
    """Main function to run the script."""
    # This function is now deprecated in favor of the GUI.
    # It is kept for backwards compatibility and simple command-line usage.
    print("Running in command-line mode. For more features, please use the GUI (run gui.py).")

    from plugins.instagram import InstagramPlugin
    instagram_plugin = InstagramPlugin()

    proxies = load_config()
    username = input("Enter Instagram username: ")
    if not username:
        return

    posts = instagram_plugin.get_posts(username, proxies=proxies)

    if posts is not None:
        if posts:
            print("\n--- Found Posts ---")
            for i, post_url in enumerate(posts):
                print(f"{i+1}: {post_url}")
            print("-------------------\n")

            save_option = input("Save posts to a file? (y/n): ").lower()
            if save_option == 'y':
                save_posts_to_file(username, posts)

            download_option = input("Download media? (y/n): ").lower()
            if download_option == 'y':
                instagram_plugin.download_posts(username, posts, proxies=proxies)
        else:
            print("No collaborated posts found.")

if __name__ == "__main__":
    main()
