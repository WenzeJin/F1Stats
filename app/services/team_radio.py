# services/team_radio.py
import requests
from typing import List
from app.models.team_radio import TeamRadio

def get_team_radio_by_session(session_id: int) -> List[TeamRadio]:
    url = "https://api.openf1.org/v1/team_radio"
    params = {"session_key": session_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        TeamRadio(
            date=item.get("date"),
            driver_number=item.get("driver_number"),
            meeting_key=item.get("meeting_key"),
            recording_url=item.get("recording_url"),
            session_key=item.get("session_key"),
        )
        for item in data
    ]

