from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Habit, HabitLog, Reminder, Category
from datetime import datetime
from app.utils import get_today_central, get_now_central
import re

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')

@habits_bp.route('/add', methods=['POST'])
@login_required
def add_habit():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '').strip()
    custom_category = request.form.get('custom_category', '').strip()
    color = request.form.get('color', '').strip()

    # Input validation
    errors = []
    if not name or len(name) > 100:
        errors.append('Habit name is required and must be less than 100 characters')
    if category and len(category) > 50:
        errors.append('Category must be less than 50 characters')
    if custom_category and len(custom_category) > 50:
        errors.append('Custom category must be less than 50 characters')
    if color and len(color) > 20:
        errors.append('Color must be less than 20 characters')

    # Validate color format (basic check for CSS color names/classes)
    if color and not re.match(r'^[a-zA-Z0-9_-]+$', color):
        errors.append('Invalid color format')

    if errors:
        flash('; '.join(errors))
        return redirect(url_for('main.dashboard'))

    category_value = custom_category or category or 'personal'

    if custom_category:
        existing_cat = Category.query.filter_by(user_id=current_user.id, name=custom_category).first()
        if not existing_cat:
            new_cat = Category(user_id=current_user.id, name=custom_category)
            db.session.add(new_cat)

    habit = Habit(name=name, category=category_value, color=color or 'blue-500', author=current_user)
    db.session.add(habit)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@habits_bp.route('/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_habit(id):
    habit = Habit.query.get_or_404(id)
    if habit.author != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    date_str = request.json.get('date') if request.json else None
    
    # Validate date format if provided
    if date_str:
        try:
            # Basic date format validation (YYYY-MM-DD)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                return jsonify({'error': 'Invalid date format'}), 400
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date'}), 400
    else:
        date = get_today_central()
    
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
    order = request.json.get('order') if request.json else None
    
    # Validate order data
    if not order or not isinstance(order, list):
        return jsonify({'error': 'Invalid order data'}), 400
    
    if len(order) > 100:  # Reasonable limit
        return jsonify({'error': 'Too many items to reorder'}), 400
    
    # Validate that all items are integers
    if not all(isinstance(habit_id, int) for habit_id in order):
        return jsonify({'error': 'Invalid habit IDs'}), 400
    
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


@habits_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    name = request.form.get('name', '').strip()
    if not name or len(name) > 50:
        flash('Category name is required and must be 1-50 characters')
        return redirect(url_for('main.settings'))

    if Category.query.filter_by(user_id=current_user.id, name=name).first():
        flash('Category already exists')
        return redirect(url_for('main.settings'))

    category = Category(user_id=current_user.id, name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('main.settings'))


@habits_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    # Remove category from habits where used
    Habit.query.filter_by(category=category.name, user_id=current_user.id).update({'category': 'personal'})
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('main.settings'))



@habits_bp.route('/reminders/add', methods=['POST'])
@login_required
def add_reminder():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date_str = request.form.get('due_date', '').strip()

    if not title or len(title) > 120:
        flash('Reminder title is required and must be <= 120 chars')
        return redirect(url_for('main.settings'))

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid due date format, use YYYY-MM-DD')
            return redirect(url_for('main.settings'))

    reminder = Reminder(user_id=current_user.id, title=title, description=description, due_date=due_date)
    db.session.add(reminder)
    db.session.commit()
    return redirect(url_for('main.settings'))


@habits_bp.route('/reminders/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    reminder.is_done = not reminder.is_done
    db.session.commit()
    return jsonify({'status': 'success', 'is_done': reminder.is_done})


@habits_bp.route('/reminders/<int:id>/delete', methods=['POST'])
@login_required
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(reminder)
    db.session.commit()
    return redirect(url_for('main.settings'))
