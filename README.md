# Social Media Timer & Blocker

## Overview

The Social Media Timer & Blocker is a desktop application designed to help users manage their time spent on social media websites. The application provides a graphical user interface (GUI) built with Tkinter, allowing users to set timers for specific social media platforms and block access to these sites once the timer expires.

## Features

- **Timer Functionality**: Set a specific amount of time allowed for each social media platform.
- **Site Blocking**: Modify the system's hosts file to block access to social media sites.
- **Cooldown Period**: Enforce a cooldown period before the user can access the site again.
- **Notifications**: Receive desktop notifications when the timer expires and when the cooldown period ends.
- **Settings Persistence**: Save user settings and timer states to a JSON file.

## Requirements

- Python 3.x
- `plyer` library for notifications
- Administrative privileges to modify the hosts file

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/social-media-timer-blocker.git
    cd social-media-timer-blocker
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application with administrative privileges:
    ```sh
    python main.py
    ```

2. Use the GUI to set timers for each social media platform and block/unblock sites as needed.

## Project Structure

- [main.py](http://_vscodecontentref_/1): Entry point of the application.
- [config](http://_vscodecontentref_/2): Configuration files.
  - [app_config.py](http://_vscodecontentref_/3): Contains configuration settings for the application.
- [src](http://_vscodecontentref_/4): Source code for the application.
  - [app.py](http://_vscodecontentref_/5): Main logic and GUI setup.
  - [gui.py](http://_vscodecontentref_/6): GUI components.
  - [site_blocker.py](http://_vscodecontentref_/7): Functionality for blocking and unblocking sites.
  - [window_manager.py](http://_vscodecontentref_/8): Utility functions for managing and monitoring active windows.
- [tests](http://_vscodecontentref_/9): Unit tests for the application.
- [logs](http://_vscodecontentref_/10): Log files.
- [settings.json](http://_vscodecontentref_/11): JSON file to save user settings and timer states.