from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from .services import AdminService
from flask_jwt_extended import jwt_required

blp = Blueprint('admin', __name__, description='Admin operations')

@blp.route('/api/check_attendance', methods=['GET'])
# @jwt_required()
def check_attendance():
    return jsonify({"attendance": AdminService.check_attendance()})

@blp.route('/students', methods=['GET'])
# @jwt_required() # Uncomment to enforce admin login
def get_students():
    return jsonify({"students": AdminService.get_all_students()})

@blp.route('/register_student', methods=['POST'])
# @jwt_required()
def register_student():
    data = request.get_json()
    if not data:
        abort(400, message="No data provided")
    return jsonify(AdminService.register_student(data))

@blp.route('/upload', methods=['POST'])
# @jwt_required()
def upload_video():
    if 'video' not in request.files:
        abort(400, message="No video file part")
    file = request.files['video']
    return jsonify(AdminService.upload_video(file))

@blp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "admin-service"})
