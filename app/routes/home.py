from flask import Blueprint, render_template
from app.services.sessions import get_all_sessions
from app.models.session import Session


home_bp = Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def index():
    sessions: list[Session] = get_all_sessions()
    sessions.sort(key=lambda s: s.date_start)
    return render_template('home/index.html', sessions=sessions)

