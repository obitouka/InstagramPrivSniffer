import requests

def get_posts(username):
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    headers = {
        "X-IG-App-ID": "936619743392459",
        "Referer": f"https://www.instagram.com/{username}/"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed: ", response.status_code)
            return

        edges = response.json()["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

        i = 0
        while i < len(edges):
            shortcode = edges[i]["node"]["shortcode"]
            print(f"{i+1}: https://www.instagram.com/p/{shortcode}")
            i += 1

    except Exception as e:
        print("Error:", str(e))

print("WARNING: THIS ONLY GIVES THE LINK OF MEDIAS WHICH ARE BEING COLLABORATED")
username = input("Enter Instagram username: ")
get_posts(username)
