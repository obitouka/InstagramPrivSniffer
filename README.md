# Media Viewer and Analyzer

This project is a powerful, web-based tool for fetching, storing, and analyzing media post information from various social media platforms via a flexible plugin system. It has evolved from a simple script into a multi-user web application with a database, a real-time progress dashboard, and data visualization capabilities.

## Features

- **Plugin-Based Architecture:** Easily extend the application to support new platforms by creating new plugins. Comes with a default plugin for Instagram.
- **Web-Based UI:** A clean and modern web interface for interacting with the application, built with Flask.
- **Multi-User Accounts:** A full user registration and login system to keep each user's data private.
- **Persistent Storage:** All collected data is stored in a robust SQLite database.
- **Real-Time Progress:** A dynamic progress bar provides real-time feedback during long-running data fetching operations.
- **Data Visualization:** A dashboard page visualizes the collected data, showing metrics like posts per user.
- **Production-Ready Deployment:** The application is configured to run in a production environment using Docker and Gunicorn.
- **Automated Test Suite:** A comprehensive test suite using pytest ensures code quality and reliability.

## Getting Started

There are two primary ways to run the application: via Docker (recommended for most users) or by setting up a local development environment.

### Docker Deployment (Recommended)

This is the easiest and most reliable way to get the application running.

1.  **Build the Docker Image:**
    From the root of the project directory, run:
    ```sh
    docker build -t media-viewer .
    ```

2.  **Run the Docker Container:**
    ```sh
    docker run -d -p 5000:5000 --name media-viewer-container -v $(pwd)/media_data.db:/app/media_data.db media-viewer
    ```
    - `-d` runs the container in detached mode (in the background).
    - `-p 5000:5000` maps port 5000 on your host to port 5000 in the container.
    - `--name media-viewer-container` gives the container a memorable name.
    - `-v $(pwd)/media_data.db:/app/media_data.db` mounts the database file from your current directory into the container, ensuring your data persists even if you remove the container.

3.  **Access the Application:**
    Open your web browser and navigate to `http://localhost:5000`.

### Local Development Setup

If you want to modify the code or contribute to the project, you should set up a local development environment.

1.  **Clone the Repository:**
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Install all the required packages from `requirements.txt`.
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the Development Server:**
    ```sh
    python app.py
    ```
    The application will be running in debug mode at `http://localhost:5000`.

## Usage

1.  **Register:** When you first access the application, you will be redirected to the login page. Click the link to register a new account.
2.  **Login:** Log in with your newly created credentials.
3.  **Fetch Posts:** On the main page, select a platform from the dropdown menu (e.g., "Instagram") and enter one or more usernames separated by commas. Click "Fetch Posts".
4.  **View Progress:** You will see a real-time progress bar as the application fetches data for each user.
5.  **View Data:** Once fetching is complete, the page will reload, and you will see the newly collected posts in the list.
6.  **View Dashboard:** Click the "Dashboard" link in the navigation bar to see a visual breakdown of the data you have collected.

## Running Tests

A comprehensive test suite is included to ensure the application is working correctly. To run the tests, make sure you have set up a local development environment and installed all dependencies.

Then, from the root of the project directory, run:
```sh
python -m pytest
```
