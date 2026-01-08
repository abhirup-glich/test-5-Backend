from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import UserModel
from ..schemas import UserSchema
from flask import abort

user_bp = Blueprint('user', __name__, url_prefix='/user', description='User operations')

@user_bp.route('/profile')
class UserProfile(MethodView):
    decorators = [jwt_required()]
    
    @user_bp.response(200, UserSchema)
    def get(self):
        """Get user profile"""
        user_id = get_jwt_identity()
        user = UserModel.get_by_id(user_id)
        if not user:
            abort(404, message="User not found")
        return user
