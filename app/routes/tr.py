from flask import Blueprint, render_template, request
from app.services.team_radio import get_team_radio_by_session
from app.services.sessions import get_session
from app.services.driver import get_id_driver_dict

tr_bp = Blueprint('tr', __name__, url_prefix='/')

@tr_bp.route('/tr')
def team_radio():
    session_id = request.args.get('session_id', type=int)
    radios = []
    session = None
    if session_id:
        radios = get_team_radio_by_session(session_id)
        session = get_session(session_id)

    id_to_driver = get_id_driver_dict()

    return render_template('home/team_radio.html', radios=radios, session=session, id_to_driver=id_to_driver)
