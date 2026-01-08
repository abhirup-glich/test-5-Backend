from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.auth_service import AuthService
from ..schemas import RegisterSchema, LoginSchema, ChangePasswordSchema, AuthResponseSchema, UserResponseSchema
from ..extensions import limiter

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', description='Authentication operations')

@auth_bp.route('/register')
class Register(MethodView):
    @auth_bp.arguments(RegisterSchema)
    @auth_bp.response(201, UserResponseSchema)
    def post(self, data):
        """Register a new user"""
        user = AuthService.register_user(data)
        return {"user": user}

@auth_bp.route('/login')
class Login(MethodView):
    decorators = [limiter.limit("5 per minute")]
    
    @auth_bp.arguments(LoginSchema)
    @auth_bp.response(200, AuthResponseSchema)
    def post(self, data):
        """Login user"""
        return AuthService.login_user(data['email'], data['password'])

@auth_bp.route('/admin-login-init')
class AdminLoginInit(MethodView):
    @auth_bp.arguments(AdminLoginInitSchema)
    @auth_bp.response(200, description="OTP sent")
    def post(self, data):
        """Initialize admin login (send OTP)"""
        return AuthService.init_admin_login(data['email'])

@auth_bp.route('/admin-login-verify')
class AdminLoginVerify(MethodView):
    @auth_bp.arguments(AdminLoginVerifySchema)
    @auth_bp.response(200, AuthResponseSchema)
    def post(self, data):
        """Verify admin login"""
        return AuthService.verify_admin_login(data['email'], data['password'], data['otp'])

@auth_bp.route('/change-password')
class ChangePassword(MethodView):
    decorators = [jwt_required()]
    
    @auth_bp.arguments(ChangePasswordSchema)
    @auth_bp.response(200, description="Password changed successfully")
    def post(self, data):
        """Change password"""
        user_id = get_jwt_identity()
        return AuthService.change_password(user_id, data['old_password'], data['new_password'])
