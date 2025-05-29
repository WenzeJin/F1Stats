# models/team_radio.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class TeamRadio:
    date: str
    driver_number: int
    meeting_key: int
    recording_url: str
    session_key: int

