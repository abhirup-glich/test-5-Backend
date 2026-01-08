from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from .services import AuthService

blp = Blueprint('auth', __name__, description='Authentication operations')

@blp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify(AuthService.register_student(data))

@blp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, message="Email and password required")
    return jsonify(AuthService.login_student(data['email'], data['password']))

@blp.route('/admin-login-init', methods=['POST'])
def admin_login_init():
    data = request.get_json()
    if not data or 'email' not in data:
        abort(400, message="Email is required")
    return AuthService.init_admin_login(data['email'])

@blp.route('/admin-login-verify', methods=['POST'])
def admin_login_verify():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data or 'otp' not in data:
        abort(400, message="Email, password, and OTP are required")
    return AuthService.verify_admin_login(data['email'], data['password'], data['otp'])

@blp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "auth-service"})
