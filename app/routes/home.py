from flask import Blueprint, render_template, request
from app.services.meeting import get_all_meetings


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def index():
    meetings = get_all_meetings()
    meetings.sort(key=lambda m: m.date_start, reverse=True)
    return render_template('home/index.html', meetings=meetings)

@home_bp.route('/sessions')
def sessions():
    from app.services.sessions import get_all_sessions
    from app.models.session import Session
    meeting_key = request.args.get('meeting_key', type=int)
    all_sessions: list[Session] = get_all_sessions()
    sessions = [s for s in all_sessions if s.meeting_key == meeting_key] if meeting_key else all_sessions
    sessions.sort(key=lambda s: s.date_start)
    return render_template('home/sessions.html', sessions=sessions)

