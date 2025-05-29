from flask import Blueprint, render_template, request, jsonify
import requests
from app.services.driver import get_id_driver_dict

live_bp = Blueprint('live', __name__, url_prefix='/')

@live_bp.route('/live')
def live_view():
    session_id = request.args.get('session_id', type=int)
    id_to_driver = get_id_driver_dict()
    return render_template('home/live.html', session_id=session_id, id_to_driver=id_to_driver)

@live_bp.route('/live_data')
def live_data():
    session_id = request.args.get('session_id', type=int)
    if not session_id:
        return jsonify({"error": "No session_id provided"}), 400
    # 一次性获取所有该 session 的圈速
    url = f"https://api.openf1.org/v1/laps?session_key={session_id}"
    resp = requests.get(url, timeout=5)
    if resp.status_code != 200:
        return jsonify([])
    all_laps = resp.json()
    # 按 driver_number 分组，取每个车手的最新一圈
    latest_lap_by_driver = {}
    for lap in all_laps:
        dn = lap.get('driver_number')
        if dn is None:
            continue
        if dn not in latest_lap_by_driver or lap.get('lap_number', 0) > latest_lap_by_driver[dn].get('lap_number', 0):
            latest_lap_by_driver[dn] = lap
    laps = list(latest_lap_by_driver.values())
    laps.sort(key=lambda l: l['driver_number'])
    return jsonify(laps)

@live_bp.route('/live_best_laps')
def live_best_laps():
    session_id = request.args.get('session_id', type=int)
    if not session_id:
        return jsonify({"error": "No session_id provided"}), 400
    url = f"https://api.openf1.org/v1/laps?session_key={session_id}"
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return jsonify([])
    all_laps = resp.json()
    # 按 driver_number 分组，取每个车手的最快圈速
    best_lap_by_driver = {}
    for lap in all_laps:
        dn = lap.get('driver_number')
        if dn is None or lap.get('lap_duration') is None:
            continue
        if dn not in best_lap_by_driver or lap['lap_duration'] < best_lap_by_driver[dn]['lap_duration']:
            best_lap_by_driver[dn] = lap
    # 只返回 driver_number 和 lap_duration
    result = {str(dn): best_lap_by_driver[dn]['lap_duration'] for dn in best_lap_by_driver}
    return jsonify(result)
