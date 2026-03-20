from app import create_app, db
from app.models import User, Habit, HabitLog, Reminder, Category

app = create_app()
with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("Done!")
