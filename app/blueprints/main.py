from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Habit, HabitLog, Reminder
from app.utils import get_today_central

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        today = get_today_central()
        habits = current_user.habits.filter_by(is_archived=False).order_by(Habit.position).all()
        completed_ids = [log.habit_id for log in HabitLog.query.filter_by(date=today).all()]
        return render_template('dashboard/index.html', habits=habits, completed_ids=completed_ids, today=today)
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    today = get_today_central()
    habits = current_user.habits.filter_by(is_archived=False).order_by(Habit.position).all()
    completed_ids = [log.habit_id for log in HabitLog.query.filter_by(date=today).all()]

    # Reminders for the current user
    reminders = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.due_date.asc(), Reminder.created_at.desc()).all()

    return render_template(
        'dashboard/index.html',
        habits=habits,
        completed_ids=completed_ids,
        today=today,
        reminders=reminders
    )
