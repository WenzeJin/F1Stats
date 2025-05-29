import sqlite3
from typing import List
from pathlib import Path
from datetime import datetime

class Database:
    def __init__(self, db_path="data/f1stats.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.create_sessions_table()
        self.create_metadata_table()

    def create_sessions_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_key INTEGER PRIMARY KEY,
            meeting_key INTEGER,
            location TEXT,
            date_start TEXT,
            date_end TEXT,
            session_type TEXT,
            session_name TEXT,
            country_key INTEGER,
            country_code TEXT,
            country_name TEXT,
            circuit_key INTEGER,
            circuit_short_name TEXT,
            gmt_offset TEXT,
            year INTEGER
        )
        ''')
        self.conn.commit()

    def create_metadata_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        self.conn.commit()

    def create_drivers_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            driver_number INTEGER PRIMARY KEY,
            broadcast_name TEXT,
            country_code TEXT,
            first_name TEXT,
            full_name TEXT,
            headshot_url TEXT,
            last_name TEXT,
            meeting_key INTEGER,
            name_acronym TEXT,
            session_key INTEGER,
            team_colour TEXT,
            team_name TEXT
        )
        ''')
        self.conn.commit()

    def create_meetings_table(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            meeting_key INTEGER PRIMARY KEY,
            circuit_key INTEGER,
            circuit_short_name TEXT,
            country_code TEXT,
            country_key INTEGER,
            country_name TEXT,
            date_start TEXT,
            gmt_offset TEXT,
            location TEXT,
            meeting_name TEXT,
            meeting_official_name TEXT,
            year INTEGER
        )
        ''')
        self.conn.commit()

    def update_last_fetch_time(self, key: str, time: datetime):
        self.conn.execute("REPLACE INTO metadata (key, value) VALUES (?, ?)", (key, time.isoformat()))
        self.conn.commit()

    def get_last_fetch_time(self, key: str) -> datetime | None:
        row = self.conn.execute("SELECT value FROM metadata WHERE key = ?", (key,)).fetchone()
        return datetime.fromisoformat(row[0]) if row else None

    def save_sessions(self, sessions: List[dict]):
        self.conn.executemany('''
        REPLACE INTO sessions VALUES (
            :session_key, :meeting_key, :location, :date_start, :date_end,
            :session_type, :session_name, :country_key, :country_code, :country_name,
            :circuit_key, :circuit_short_name, :gmt_offset, :year
        )
        ''', sessions)
        self.conn.commit()

    def load_sessions(self) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM sessions")
        columns = [desc[0] for desc in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

    def save_drivers(self, drivers: list[dict]):
        self.create_drivers_table()
        self.conn.execute('DELETE FROM drivers')
        for d in drivers:
            self.conn.execute('''
                INSERT OR REPLACE INTO drivers (
                    driver_number, broadcast_name, country_code, first_name, full_name, headshot_url, last_name, meeting_key, name_acronym, session_key, team_colour, team_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                d.get('driver_number'), d.get('broadcast_name'), d.get('country_code'), d.get('first_name'), d.get('full_name'),
                d.get('headshot_url'), d.get('last_name'), d.get('meeting_key'), d.get('name_acronym'), d.get('session_key'),
                d.get('team_colour'), d.get('team_name')
            ))
        self.conn.commit()

    def load_drivers(self) -> list[dict]:
        self.create_drivers_table()
        cursor = self.conn.execute('SELECT * FROM drivers')
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def save_meetings(self, meetings: list[dict]):
        self.create_meetings_table()
        self.conn.execute('DELETE FROM meetings')
        for m in meetings:
            self.conn.execute('''
                INSERT OR REPLACE INTO meetings (
                    meeting_key, circuit_key, circuit_short_name, country_code, country_key, country_name, date_start, gmt_offset, location, meeting_name, meeting_official_name, year
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                m.get('meeting_key'), m.get('circuit_key'), m.get('circuit_short_name'), m.get('country_code'), m.get('country_key'),
                m.get('country_name'), m.get('date_start'), m.get('gmt_offset'), m.get('location'), m.get('meeting_name'),
                m.get('meeting_official_name'), m.get('year')
            ))
        self.conn.commit()

    def load_meetings(self) -> list[dict]:
        self.create_meetings_table()
        cursor = self.conn.execute('SELECT * FROM meetings')
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

