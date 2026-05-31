# Todo
- [ ] Clean up (e.g. type casting, restructures, etc.)
- [ ] Set up CI/CD for the project
- [ ] Write unit and integration tests
- [ ] Create the C++ server
- [ ] Add some analytics for spotify app

Stretch
- [ ] Containerize the application
- [ ] Weather/ Daily activity app with Apple Watch

# Cozy display

A Django app that integrates with Google Calendar and Spotify and fetches misc data for display/ personal use. I fetched these data and use them on an E-ink display, connected to a 
Raspberry Pi 3 using a C++ server (tbu)

## Prerequisites

- Python 3.12+
- A Google Cloud project with the **Google Calendar API** enabled and OAuth 2.0 credentials configured

## Resources

- Google calendar API documentations: https://developers.google.com/workspace/calendar/api/guides/overview
- Spotify documentations: https://developer.spotify.com/documentation/web-api

## Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **OAuth consent screen**
2. Set the app to **Testing** mode and add your Google account under **Test users**
3. Go to **Credentials** → **Create Credentials** → **OAuth client ID** (type: Web application)
4. Add `http://127.0.0.1:8000/calendar/oauth/callback/` as an authorized redirect URI
5. Download the credentials JSON and place it in the project root as `credentials.json`

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

## Endpoints
Check out the `views` folder in the googlecalendar and spotify apps. 

## Running the App

```bash
source venv/bin/activate
python manage.py runserver
```

## Formatting and linting
This project uses ruff for formatting
- ``ruff check`` for linting checks
- ``ruff format`` to format your files 

Then open `http://127.0.0.1:8000` in your browser.

## Tips

- To avoid generating `__pycache__` files, set `PYTHONDONTWRITEBYTECODE=1` before running the server
- To deactivate the virtual environment, run `deactivate`
