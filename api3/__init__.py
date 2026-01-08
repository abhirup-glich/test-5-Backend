from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from .config import Config

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    jwt.init_app(app)
    
    from .routes import admin_bp
    app.register_blueprint(admin_bp)

    from .monitoring import register_monitoring
    register_monitoring(app)
    
    return app
