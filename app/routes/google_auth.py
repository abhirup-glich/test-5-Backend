from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
import firebase_admin
from firebase_admin import credentials, auth
from ..services.auth_service import AuthService
from ..schemas import AuthResponseSchema, UserSchema

# Initialize Firebase Admin
# Note: In production, use environment variables or a service account file
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# For now, we'll assume it's initialized elsewhere or use default credentials if on Google Cloud
if not firebase_admin._apps:
    firebase_admin.initialize_app()

google_auth_bp = Blueprint('google_auth', __name__, url_prefix='/auth', description='Google Authentication')

@google_auth_bp.route('/google-login')
class GoogleLogin(MethodView):
    @google_auth_bp.response(200, AuthResponseSchema)
    def post(self):
        """Login with Google ID Token"""
        data = request.get_json()
        id_token = data.get('id_token')
        
        if not id_token:
            abort(400, message="ID token is required")
            
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            email = decoded_token['email']
            name = decoded_token.get('name', '')
            uid = decoded_token['uid']
            
            # Check if user exists in our DB, if not register them
            # This logic should be in AuthService, but for brevity:
            user = AuthService.get_user_by_email(email)
            if not user:
                # Register new user
                user_data = {
                    'name': name,
                    'email': email,
                    'password': uid, # Use UID as temporary password or handle passwordless
                    'unique_id': uid,
                    'course': 'Unknown' # Placeholder
                }
                user = AuthService.register_user(user_data)
                
            # Login user
            return AuthService.login_user(email, uid) # Assuming password check passes or we bypass
            
        except Exception as e:
            abort(401, message=f"Invalid token: {str(e)}")
