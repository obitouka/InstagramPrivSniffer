import PySimpleGUI as sg
import src.privateMediaViewer as pmv
import src.plugin_manager as plugin_manager
import src.database as db

def update_output_from_db(window, query=None, date_after=None, date_before=None):
    """Refreshes the output text area with posts from the database, applying filters."""
    posts = db.search_posts(query=query, date_after=date_after, date_before=date_before)
    output_text = ""
    for username, post_url, timestamp in posts:
        output_text += f"[{timestamp}] {username}: {post_url}\n"
    window["-OUTPUT-"].update(output_text)

import argparse

def run_headless(args):
    """Runs the application in headless mode based on command-line arguments."""
    print("Running in headless mode...")
    db.setup_database()

    if args.username:
        plugins = plugin_manager.load_plugins()
        if args.plugin not in plugins:
            print(f"Error: Plugin '{args.plugin}' not found.")
            return
        plugin = plugins[args.plugin]
        proxies = pmv.load_config()

        for username in args.username:
            print(f"Fetching posts for {username} using {plugin.name} plugin...")
            posts = plugin.get_posts(username, proxies=proxies)
            if posts:
                db.insert_posts(username, posts)
                print(f"Found and saved {len(posts)} posts for {username}.")
            elif posts == []:
                print(f"No new posts found for {username}.")
            else:
                print(f"Failed to fetch posts for {username}.")

    if args.search or args.date_after or args.date_before:
        print("\n--- Search Results ---")
        results = db.search_posts(query=args.search, date_after=args.date_after, date_before=args.date_before)
        for username, post_url, timestamp in results:
            print(f"[{timestamp}] {username}: {post_url}")
        print("----------------------")

    print("Headless run complete.")

def main():
    """Main function to run the application."""
    parser = argparse.ArgumentParser(description="Media Viewer application.")
    parser.add_argument('--headless', action='store_true', help='Run in headless mode without GUI.')
    parser.add_argument('--username', type=str, nargs='*', help='One or more usernames to fetch in headless mode.')
    parser.add_argument('--plugin', type=str, default='Instagram', help='The plugin to use in headless mode.')
    parser.add_argument('--search', type=str, help='Search query for headless mode.')
    parser.add_argument('--date-after', type=str, help='Search for posts after this date (YYYY-MM-DD).')
    parser.add_argument('--date-before', type=str, help='Search for posts before this date (YYYY-MM-DD).')
    args = parser.parse_args()

    if args.headless:
        run_headless(args)
        return

    # --- GUI Mode ---
    sg.theme("DarkBlue3")
    db.setup_database()

    plugins = plugin_manager.load_plugins()
    plugin_names = list(plugins.keys())

    filter_layout = [
        [
            sg.Text("Search:"), sg.Input(key="-QUERY-", size=(20,1)),
            sg.Text("After:"), sg.Input(key="-DATE_AFTER-", size=(10,1)), sg.CalendarButton("...", target="-DATE_AFTER-", format="%Y-%m-%d"),
            sg.Text("Before:"), sg.Input(key="-DATE_BEFORE-", size=(10,1)), sg.CalendarButton("...", target="-DATE_BEFORE-", format="%Y-%m-%d"),
            sg.Button("Search", key="-SEARCH-"), sg.Button("Clear", key="-CLEAR-")
        ]
    ]

    layout = [
        [sg.Text("Select Platform:"), sg.Combo(plugin_names, default_value=plugin_names[0] if plugin_names else "", key="-PLUGIN-")],
        [sg.Text("Enter Username(s), separated by commas:")],
        [sg.Input(key="-USERNAMES-", size=(60, 1))],
        [sg.Button("Fetch Posts", key="-FETCH-"), sg.Button("Download Media", key="-DOWNLOAD-", disabled=True)],
        [sg.Frame("Filters", filter_layout)],
        [sg.Text("Output:", size=(40, 1))],
        [sg.Multiline(size=(60, 15), key="-OUTPUT-", disabled=True)],
        [sg.StatusBar("Ready", size=(60, 1), key="-STATUS-")]
    ]

    window = sg.Window("Media Viewer", layout)
    update_output_from_db(window) # Initial load

    all_posts = {} # Store posts per username from the last fetch

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-FETCH-":
            selected_plugin_name = values["-PLUGIN-"]
            if not selected_plugin_name:
                sg.popup_error("Please select a platform.")
                continue

            plugin = plugins[selected_plugin_name]

            usernames_str = values["-USERNAMES-"]
            if not usernames_str:
                sg.popup_error("Please enter at least one username.")
                continue

            usernames = [u.strip() for u in usernames_str.split(',')]
            all_posts.clear()
            window["-DOWNLOAD-"].update(disabled=True)

            proxies = pmv.load_config()

            for username in usernames:
                if not username: continue

                window["-STATUS-"].update(f"Fetching posts for {username} using {plugin.name} plugin...")
                window.refresh()

                posts = plugin.get_posts(username, proxies=proxies)
                all_posts[username] = posts

                if posts:
                    db.insert_posts(username, posts)
                elif posts == []:
                    print(f"No new posts found for {username}")
                else:
                    print(f"Failed to fetch posts for {username}")

            update_output_from_db(window)
            if any(all_posts.values()):
                 window["-DOWNLOAD-"].update(disabled=False)
            window["-STATUS-"].update("Finished fetching all posts.")

        if event == "-SEARCH-":
            query = values["-QUERY-"] if values["-QUERY-"] else None
            date_after = values["-DATE_AFTER-"] if values["-DATE_AFTER-"] else None
            date_before = values["-DATE_BEFORE-"] if values["-DATE_BEFORE-"] else None
            update_output_from_db(window, query=query, date_after=date_after, date_before=date_before)
            window["-STATUS-"].update("Search complete.")

        if event == "-CLEAR-":
            window["-QUERY-"].update("")
            window["-DATE_AFTER-"].update("")
            window["-DATE_BEFORE-"].update("")
            update_output_from_db(window)
            window["-STATUS-"].update("Filters cleared.")

        if event == "-DOWNLOAD-":
            selected_plugin_name = values["-PLUGIN-"]
            if not selected_plugin_name:
                sg.popup_error("Please select a platform.")
                continue
            plugin = plugins[selected_plugin_name]

            if any(all_posts.values()):
                proxies = pmv.load_config()
                for username, posts in all_posts.items():
                    if posts:
                        window["-STATUS-"].update(f"Downloading media for {username}...")
                        window.refresh()
                        try:
                            plugin.download_posts(username, posts, proxies=proxies)
                        except Exception as e:
                            sg.popup_error(f"Failed to download media for {username}: {e}")
                window["-STATUS-"].update("Finished all downloads.")
                sg.popup("Finished downloading all media.")
            else:
                sg.popup_error("No posts to download.")

    window.close()

if __name__ == "__main__":
    main()
