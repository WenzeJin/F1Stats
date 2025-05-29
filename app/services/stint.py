import requests
from typing import List
from app.models.stint import Stint

def get_stints_by_session(session_key: int) -> List[Stint]:
    url = "https://api.openf1.org/v1/stints"
    params = {"session_key": session_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        Stint(
            compound=item.get("compound"),
            driver_number=item.get("driver_number"),
            lap_end=item.get("lap_end"),
            lap_start=item.get("lap_start"),
            meeting_key=item.get("meeting_key"),
            session_key=item.get("session_key"),
            stint_number=item.get("stint_number"),
            tyre_age_at_start=item.get("tyre_age_at_start"),
        )
        for item in data
    ]
