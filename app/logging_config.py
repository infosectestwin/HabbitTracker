import logging
import json
from datetime import datetime
from flask import request, g, has_request_context
from flask_login import current_user


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(app):
    """Configure JSON logging for the Flask app."""
    
    # Create logger
    logger = logging.getLogger('habbit_tracker')
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler with JSON formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    return logger


def setup_request_logging(app):
    """Add request/response logging middleware to Flask app."""
    
    logger = logging.getLogger('habbit_tracker')
    
    @app.before_request
    def log_request_start():
        """Log incoming request."""
        g.start_time = datetime.utcnow()
        
    @app.after_request
    def log_request_end(response):
        """Log outgoing response with duration and metadata."""
        if not has_request_context():
            return response
        
        # Calculate request duration
        start_time = g.pop('start_time', None)
        if start_time:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        else:
            duration_ms = 0
        
        # Get user ID if authenticated
        user_id = current_user.id if current_user.is_authenticated else None
        
        # Get client IP (best effort: check X-Forwarded-For first for proxies)
        client_ip = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
        if not client_ip:
            client_ip = request.remote_addr or 'unknown'
        
        # Build structured log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': 'INFO',
            'type': 'http_request',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration_ms, 2),
            'client_ip': client_ip,
            'user_id': user_id,
        }
        
        logger.info(json.dumps(log_entry))
        return response
