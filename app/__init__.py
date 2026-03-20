from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from app.logging_config import setup_logging, setup_request_logging

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

    # Initialize logging
    setup_logging(app)
    setup_request_logging(app)

    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        """
        Add secure default HTTP headers to all responses.
        
        Headers included:
        - Content-Security-Policy: Restrictive policy for security
        - X-Content-Type-Options: Prevents MIME type sniffing
        - X-Frame-Options: Prevents clickjacking attacks
        - Referrer-Policy: Controls referrer information sent in requests
        - Strict-Transport-Security: Enforces HTTPS (only when request is HTTPS)
        """
        # Generate a nonce for inline scripts/styles
        import secrets
        nonce = secrets.token_hex(16)
        
        # Store nonce in request context for templates
        g.csp_nonce = nonce
        
        # Content Security Policy - restrictive but functional
        response.headers['Content-Security-Policy'] = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{nonce}' https://unpkg.com https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
            f"style-src 'self' 'nonce-{nonce}' https://fonts.googleapis.com; "
            f"img-src 'self' data: https:; "
            f"font-src 'self' https://fonts.gstatic.com; "
            f"connect-src 'self'; "
            f"frame-ancestors 'none';"
        )
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Control referrer information
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # HTTP Strict Transport Security (only for HTTPS requests)
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response

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
