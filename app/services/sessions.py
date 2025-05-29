import requests
from datetime import datetime, timedelta, UTC
from app.models.session import Session
from app.services.database import Database

SESSION_CACHE_KEY = "last_session_fetch"
CACHE_EXPIRY = timedelta(hours=6)

def get_all_sessions() -> list[Session]:
    db = Database()

    last_fetch = db.get_last_fetch_time(SESSION_CACHE_KEY)
    now = datetime.now(UTC)

    if last_fetch and now - last_fetch < CACHE_EXPIRY:
        print("Loaded sessions from DB cache")
        session_dicts = db.load_sessions()
    else:
        print("Fetching sessions from API")
        # get current year
        current_year = now.year
        resp = requests.get(f"https://api.openf1.org/v1/sessions?year={current_year}", timeout=10)
        session_dicts = resp.json()

        db.save_sessions(session_dicts)
        db.update_last_fetch_time(SESSION_CACHE_KEY, now)

    return [Session(**s) for s in session_dicts]

def get_session(session_id: str | int) -> Session | None:
    sessions = get_all_sessions()
    for session in sessions:
        if session.session_key == int(session_id):
            return session
    return None