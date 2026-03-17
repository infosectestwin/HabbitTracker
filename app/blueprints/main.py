from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Habit, HabitLog
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
    # Logic to fetch habits and status for today
    habits = current_user.habits.filter_by(is_archived=False).order_by(Habit.position).all()
    # We need to pass which habits are completed today
    completed_ids = [log.habit_id for log in HabitLog.query.filter_by(date=today).all()]
    
    return render_template('dashboard/index.html', habits=habits, completed_ids=completed_ids, today=today)
