from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Habit, HabitLog
from datetime import datetime
from app.utils import get_today_central, get_now_central

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')

@habits_bp.route('/add', methods=['POST'])
@login_required
def add_habit():
    name = request.form.get('name')
    category = request.form.get('category')
    color = request.form.get('color')
    # Add validation
    
    habit = Habit(name=name, category=category, color=color, author=current_user)
    db.session.add(habit)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@habits_bp.route('/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_habit(id):
    habit = Habit.query.get_or_404(id)
    if habit.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    date_str = request.json.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else get_today_central()
    
    log = HabitLog.query.filter_by(habit_id=habit.id, date=date).first()
    
    if log:
        db.session.delete(log)
        status = 'unchecked'
    else:
        log = HabitLog(habit=habit, date=date, completed_at=get_now_central())
        db.session.add(log)
        status = 'checked'
        
    db.session.commit()
    return jsonify({'status': status, 'habit_id': id})

@habits_bp.route('/reorder', methods=['POST'])
@login_required
def reorder_habits():
    order = request.json.get('order') # List of habit IDs
    for index, habit_id in enumerate(order):
        habit = Habit.query.get(habit_id)
        if habit and habit.author == current_user:
            habit.position = index
    db.session.commit()
    return jsonify({'status': 'success'})

@habits_bp.route('/<int:id>/archive', methods=['POST'])
@login_required
def archive_habit(id):
    habit = Habit.query.get_or_404(id)
    if habit.author == current_user:
        habit.is_archived = True
        db.session.commit()
    return redirect(url_for('main.dashboard'))
