import PySimpleGUI as sg
import privateMediaViewer as pmv

def main():
    """Main function to run the GUI application."""
    sg.theme("DarkBlue3")

    layout = [
        [sg.Text("Enter Instagram Username:")],
        [sg.Input(key="-USERNAME-", size=(30, 1))],
        [sg.Button("Fetch Posts", key="-FETCH-"), sg.Button("Save to File", key="-SAVE-", disabled=True)],
        [sg.Text("Output:", size=(40, 1))],
        [sg.Multiline(size=(60, 15), key="-OUTPUT-", disabled=True)],
        [sg.StatusBar("Ready", size=(60, 1), key="-STATUS-")]
    ]

    window = sg.Window("Instagram Collaborated Posts Viewer", layout)

    posts = []
    username = ""

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-FETCH-":
            username = values["-USERNAME-"]
            if not username:
                sg.popup_error("Please enter a username.")
                continue

            window["-STATUS-"].update(f"Fetching posts for {username}...")
            window["-OUTPUT-"].update("")
            window.refresh() # Force window to update

            posts = pmv.get_posts(username)

            if posts is not None:
                if posts:
                    output_text = "\n".join([f"{i+1}: {url}" for i, url in enumerate(posts)])
                    window["-OUTPUT-"].update(output_text)
                    window["-SAVE-"].update(disabled=False)
                    window["-STATUS-"].update(f"Successfully fetched {len(posts)} posts.")
                else:
                    window["-OUTPUT-"].update("No collaborated posts found.")
                    window["-SAVE-"].update(disabled=True)
                    window["-STATUS-"].update("No posts found.")
            else:
                window["-OUTPUT-"].update("Failed to fetch posts. See console for details.")
                window["-SAVE-"].update(disabled=True)
                window["-STATUS-"].update("Error fetching posts.")

        if event == "-SAVE-":
            if posts and username:
                try:
                    pmv.save_posts_to_file(username, posts)
                    window["-STATUS-"].update(f"Posts saved to {username}_posts.txt")
                    sg.popup(f"Successfully saved posts to {username}_posts.txt")
                except Exception as e:
                    sg.popup_error(f"Error saving file: {e}")
                    window["-STATUS-"].update("Error saving file.")
            else:
                sg.popup_error("No posts to save.")

    window.close()

if __name__ == "__main__":
    main()
