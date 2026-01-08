from flask import Flask
from flask_cors import CORS
import os

from .config import Config
from .extensions import bcrypt, jwt, limiter, api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, supports_credentials=True)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    api.init_app(app)
    
    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.legacy import legacy_bp
    # from .routes.google_auth import google_auth_bp
    
    api.register_blueprint(auth_bp)
    api.register_blueprint(user_bp)
    # api.register_blueprint(google_auth_bp)
    app.register_blueprint(legacy_bp)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
