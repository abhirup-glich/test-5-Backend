from flask import Flask
from flask_cors import CORS
import os
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    from .routes import attendance_bp
    app.register_blueprint(attendance_bp)

    from .monitoring import register_monitoring
    register_monitoring(app)
    
    return app
