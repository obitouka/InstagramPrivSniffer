"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""
import requests

def get_posts(username):
    """Fetches collaborated posts for a given Instagram username."""
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "X-IG-App-ID": "936619743392459",
        "Referer": f"https://www.instagram.com/{username}/",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: Status code {response.status_code}")
            return None

        user_data = response.json()["data"]["user"]

        if user_data.get("is_private"):
            print("The profile is private. Fetching collaborated posts...")
        else:
            print("The profile is public. Fetching collaborated posts...")

        edges = user_data["edge_owner_to_timeline_media"]["edges"]

        if not edges:
            print("No collaborated posts found.")
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
    username = input("Enter Instagram username: ")
    if not username:
        return

    posts = get_posts(username)

    if posts is not None:
        if posts:
            print("\n--- Found Posts ---")
            for i, post_url in enumerate(posts):
                print(f"{i+1}: {post_url}")
            print("-------------------\n")

            save_option = input("Save posts to a file? (y/n): ").lower()
            if save_option == 'y':
                save_posts_to_file(username, posts)
        else:
            # This case is handled inside get_posts, but we keep it for clarity
            pass

if __name__ == "__main__":
    main()
