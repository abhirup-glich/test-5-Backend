from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from .services import AttendanceService

blp = Blueprint('attendance', __name__, description='Attendance operations')

@blp.route('/api/identify', methods=['POST'])
def identify():
    data = request.get_json()
    if not data or 'image' not in data:
        abort(400, message="Image data required")
    return jsonify(AttendanceService.identify_user(data['image']))

@blp.route('/api/mark-attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    if not data:
        abort(400, message="Data required")
    return jsonify(AttendanceService.mark_attendance(data))

@blp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "attendance-service"})
