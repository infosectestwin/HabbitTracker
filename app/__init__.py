from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.habits import habits_bp
    from app.blueprints.stats import stats_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(stats_bp)

    return app
