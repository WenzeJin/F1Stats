from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    meeting_key: int
    session_key: int
    location: str
    date_start: datetime
    date_end: datetime
    session_type: str
    session_name: str
    country_key: int
    country_code: str
    country_name: str
    circuit_key: int
    circuit_short_name: str
    gmt_offset: str
    year: int