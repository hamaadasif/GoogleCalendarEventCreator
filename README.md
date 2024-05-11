# Google Calendar Event Creator

This application provides a graphical user interface to create events in Google Calendar. Users can set event details such as the name, date, time, location, and attendees, and the events are added directly to their Google Calendar.

## Features

- Authenticate with Google Calendar using OAuth credentials.
- Create new calendar events with details such as date, time, location, and attendees.
- Display a confirmation popup with a link to the event in Google Calendar.

## Requirements

- Python 3.x
- Tkinter for GUI
- `tkcalendar` for date selection
- `pytz` for timezone handling
- `google-auth` and `google-auth-oauthlib` for authentication
- `google-api-python-client` for interacting with Google Calendar

## Setup

1. Install the required Python packages:

    ```bash
    pip install tkinter tkcalendar pytz google-auth google-auth-oauthlib google-api-python-client
    ```

2. Obtain OAuth 2.0 credentials from the Google API Console.
   - Create or select a project in the Google Developers Console.
   - Enable the Google Calendar API.
   - Go to "Credentials" and set up a consent screen.
   - Create credentials for a Desktop application. Download the JSON file and place it in the same directory as the script.

3. Rename the downloaded JSON file to `credentials.json`.

## Usage

1. Run the script:

    ```bash
    python main.py
    ```

2. The GUI will open, allowing you to input event details:
   - **Event Name**: Name of the event.
   - **Date**: Click "Select Date" to open a calendar popup and choose a date.
   - **Start Time** and **End Time**: Select from predefined 15-minute intervals.
   - **Location**: Location of the event.
   - **Invite**: Email addresses of the attendees, separated by commas.

3. Click "Create Event" to add the event to your Google Calendar. A confirmation popup will appear with an option to view the event.

## Additional Notes

- Ensure your `credentials.json` then `token.json` (automatically created upon successful authentication) are secured.
- The script handles token refresh automatically if the authentication expires.
