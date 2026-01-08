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
    from .routes import auth_bp
    api.register_blueprint(auth_bp)

    # Register Monitoring
    from .monitoring import register_monitoring
    register_monitoring(app)
    
    return app
