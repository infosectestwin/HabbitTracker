from app import create_app, db
from app.models import User, Habit, HabitLog
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Never run debug=True in production - use environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
else:
    # Production settings for PythonAnywhere
    app.config['DEBUG'] = False
