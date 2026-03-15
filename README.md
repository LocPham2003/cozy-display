# Smart Calendar

A Django app that integrates with Google Calendar.

## Prerequisites

- Python 3.12+
- A Google Cloud project with the **Google Calendar API** enabled and OAuth 2.0 credentials configured

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

## Running the App

```bash
source venv/bin/activate
python manage.py runserver
```

Then open `http://127.0.0.1:8000` in your browser.

## Tips

- To avoid generating `__pycache__` files, set `PYTHONDONTWRITEBYTECODE=1` before running the server
- To deactivate the virtual environment, run `deactivate`
