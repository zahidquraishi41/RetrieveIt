# RetrieveIt

RetrieveIt is a Python application designed to streamline the process of downloading and organizing saved items from your Reddit account.

## Features

- **Media Types:** Retrieve various media types, including images and videos.
- **Organized Storage:** Automatically categorize saved items by their subreddits for better organization.
- **Unsave After Download:** Optionally unsave items from Reddit after downloading by setting "unsave_after_download" to true in `config.json`.
- **Separate Folders for Media Types:** Videos and images are stored separately in folders such as `downloads/Images` and `downloads/Videos`.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/zahidquraishi41/RetrieveIt.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Obtaining Reddit API Credentials

To use RetrieveIt, you need to obtain Reddit API credentials. Follow these steps to create a Reddit application:

1. Log into your Reddit account.

2. Open [Reddit Preferences - Apps](https://www.reddit.com/prefs/apps).

3. Click on "Create Another App" and provide the following details:
   - Name: savedscrapper
   - Check the "script" radio button.
   - Redirect URL: http://localhost:8080.

4. Click on "Create."

5. Make a note of the following information:
   - Personal Use Script (Client ID)
   - Secret

## Configuration

On the first run, RetrieveIt will create a `config.json` file in the project root. Open it using a text editor to customize settings.
