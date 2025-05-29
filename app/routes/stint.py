from flask import Blueprint, render_template, request
from app.services.stint import get_stints_by_session
from app.services.sessions import get_session
from app.services.driver import get_id_driver_dict

stint_bp = Blueprint('stint', __name__, url_prefix='/')

@stint_bp.route('/stint')
def stint_view():
    session_id = request.args.get('session_id', type=int)
    stints_by_driver = {}
    session = None
    max_lap = 0
    if session_id:
        id_to_driver = get_id_driver_dict()
        all_stints = get_stints_by_session(session_id)
        for stint in all_stints:
            if stint.driver_number not in stints_by_driver:
                stints_by_driver[stint.driver_number] = []
            stints_by_driver[stint.driver_number].append(stint)
            if stint.lap_end and stint.lap_end > max_lap:
                max_lap = stint.lap_end
        # 按 stint_number 排序
        for driver_number in stints_by_driver:
            stints_by_driver[driver_number].sort(key=lambda s: s.stint_number)
        session = get_session(session_id)
    else:
        id_to_driver = {}
    return render_template('home/stint.html', stints_by_driver=stints_by_driver, session=session, id_to_driver=id_to_driver, max_lap=max_lap)
