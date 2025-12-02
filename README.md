# iTunes to Drive & YouTube Manager

A Flask-based web application that bridges iTunes Movie Trailers, Google Drive, and YouTube. It allows you to browse HD trailers, save them to your Google Drive, and upload videos from Drive to YouTube.

## Features
1.  **Browse Trailers**: Fetches and lists available HD movie trailers from iTunes.
2.  **Save to Drive**: One-click download of trailers to a specific "Apple Trailers" folder in your Google Drive.
3.  **Manage Drive Videos**: Lists video files from your "Apple Trailers" Drive folder.
4.  **Upload to YouTube**: Upload selected videos from Drive directly to a YouTube channel.

## Getting Started

### Prerequisites
- Python 3.x
- A Google Cloud Project with the following APIs enabled:
    - Google Drive API
    - YouTube Data API v3
- `credentials.json` file from your Google Cloud Project.

### Installation
1.  Clone the repository.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
1.  **Google Cloud Credentials**:
    -   Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    -   Enable **Google Drive API** and **YouTube Data API v3**.
    -   Create OAuth 2.0 Client IDs (Desktop or Web Application).
    -   Download the JSON file, rename it to `credentials.json`, and place it in the project root directory.
2.  **Google Apps Script** (Optional for "Save to Drive" feature):
    -   The "Save to Drive" feature relies on a deployed Google Apps Script. The current URL in `flask-app.py` may need to be updated with your own deployment of `Code.gs`.

### How to Run
1.  Start the Flask application:
    ```bash
    python flask-app.py
    ```
    *Or if using Flask CLI:*
    ```bash
    export FLASK_APP=flask-app.py
    flask run
    ```
2.  Open your browser and navigate to `http://localhost:5000`.

## Usage
-   **Home**: Landing page.
-   **List Trailers**: View iTunes trailers. Click a trailer to save it to Drive (requires Apps Script setup).
-   **My Drive**: Log in with Google to view videos in your "Apple Trailers" folder.
-   **Upload**: Select a video from "My Drive" to upload it to YouTube.
