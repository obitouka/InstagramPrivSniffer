import PySimpleGUI as sg
import src.privateMediaViewer as pmv
import src.plugin_manager as plugin_manager

def main():
    """Main function to run the GUI application."""
    sg.theme("DarkBlue3")

    plugins = plugin_manager.load_plugins()
    plugin_names = list(plugins.keys())

    layout = [
        [sg.Text("Select Platform:"), sg.Combo(plugin_names, default_value=plugin_names[0] if plugin_names else "", key="-PLUGIN-")],
        [sg.Text("Enter Username(s), separated by commas:")],
        [sg.Input(key="-USERNAMES-", size=(60, 1))],
        [sg.Button("Fetch Posts", key="-FETCH-"), sg.Button("Save to File", key="-SAVE-", disabled=True), sg.Button("Download Media", key="-DOWNLOAD-", disabled=True)],
        [sg.Text("Output:", size=(40, 1))],
        [sg.Multiline(size=(60, 15), key="-OUTPUT-", disabled=True)],
        [sg.StatusBar("Ready", size=(60, 1), key="-STATUS-")]
    ]

    window = sg.Window("Media Viewer", layout)

    all_posts = {} # Store posts per username

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
            window["-OUTPUT-"].update("")
            window["-SAVE-"].update(disabled=True)
            window["-DOWNLOAD-"].update(disabled=True)

            proxies = pmv.load_config()
            full_output_text = ""

            for username in usernames:
                if not username: continue

                window["-STATUS-"].update(f"Fetching posts for {username} using {plugin.name} plugin...")
                window.refresh()

                posts = plugin.get_posts(username, proxies=proxies)
                all_posts[username] = posts

                if posts:
                    full_output_text += f"--- Posts for {username} ---\n"
                    full_output_text += "\n".join([f"{i+1}: {url}" for i, url in enumerate(posts)])
                    full_output_text += "\n\n"
                elif posts == []:
                    full_output_text += f"--- No posts found for {username} ---\n\n"
                else:
                     full_output_text += f"--- Failed to fetch posts for {username} ---\n\n"

            window["-OUTPUT-"].update(full_output_text)
            if any(all_posts.values()):
                 window["-SAVE-"].update(disabled=False)
                 window["-DOWNLOAD-"].update(disabled=False)
            window["-STATUS-"].update("Finished fetching all posts.")


        if event == "-SAVE-":
            if any(all_posts.values()):
                try:
                    with open("all_users_posts.txt", "w") as f:
                        for username, posts in all_posts.items():
                            if posts:
                                f.write(f"--- Posts for {username} ---\n")
                                for i, post_url in enumerate(posts):
                                    f.write(f"{i+1}: {post_url}\n")
                                f.write("\n")

                    window["-STATUS-"].update("Posts saved to all_users_posts.txt")
                    sg.popup("Successfully saved all posts to all_users_posts.txt")
                except Exception as e:
                    sg.popup_error(f"Error saving file: {e}")
                    window["-STATUS-"].update("Error saving file.")
            else:
                sg.popup_error("No posts to save.")

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
