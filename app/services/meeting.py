import requests
from datetime import datetime, timedelta, UTC
from app.models.meeting import Meeting
from app.services.database import Database

MEETING_CACHE_KEY = "last_meeting_fetch"
CACHE_EXPIRY = timedelta(hours=24)

def get_all_meetings() -> list[Meeting]:
    db = Database()
    last_fetch = db.get_last_fetch_time(MEETING_CACHE_KEY)
    now = datetime.now(UTC)
    current_year = now.year

    if last_fetch and now - last_fetch < CACHE_EXPIRY:
        print("Loaded meetings from DB cache")
        meeting_dicts = db.load_meetings()
        # 只保留当前年份及之后的 meeting
        meeting_dicts = [m for m in meeting_dicts if int(m.get('year', 0)) >= current_year]
    else:
        print("Fetching meetings from API")
        resp = requests.get(f"https://api.openf1.org/v1/meetings?year>={current_year}", timeout=10)
        meeting_dicts = resp.json()
        db.save_meetings(meeting_dicts)
        db.update_last_fetch_time(MEETING_CACHE_KEY, now)

    return [Meeting(**m) for m in meeting_dicts]
