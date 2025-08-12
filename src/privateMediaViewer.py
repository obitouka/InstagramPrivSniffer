"""
Copyright (c) 2025 obitouka
See the file 'LICENSE' for copying permission
"""
import requests

def get_posts(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "X-IG-App-ID": "936619743392459",
        "Referer": f"https://www.instagram.com/{username}/",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed: ", response.status_code)
            return

        user_data = response.json()["data"]["user"]

        if user_data.get("is_private"):
            print("The profile is private. Fetching collaborated posts...")
        else:
            print("The profile is public. Fetching collaborated posts...")

        edges = user_data["edge_owner_to_timeline_media"]["edges"]

        if not edges:
            print("No posts found.")
            return

        for i, edge in enumerate(edges):
            shortcode = edge["node"]["shortcode"]
            print(f"{i+1}: https://www.instagram.com/p/{shortcode}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except KeyError:
        print("Could not retrieve user data. The profile may not exist or there was an API change.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """Main function to run the script."""
    # print("WARNING: Only works for media from private/public profiles with collaborations")
    username = input("Enter Instagram username: ")
    if username:
        get_posts(username)

if __name__ == "__main__":
    main()
