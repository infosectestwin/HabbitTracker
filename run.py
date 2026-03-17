from app import create_app, db
from app.models import User, Habit, HabitLog
import os

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
else:
    # Production settings for PythonAnywhere
    app.config['DEBUG'] = False
