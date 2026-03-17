from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import Habit, HabitLog
from datetime import timedelta
from app.utils import get_today_central

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')

@stats_bp.route('/')
@login_required
def index():
    return render_template('stats/index.html')

@stats_bp.route('/data')
@login_required
def get_stats_data():
    today = get_today_central()
    
    # 1. Timeline Data (Last 14 days)
    timeline_labels = []
    timeline_rates = []
    active_habits_count = current_user.habits.filter_by(is_archived=False).count()
    
    for i in range(13, -1, -1):
        date = today - timedelta(days=i)
        timeline_labels.append(date.strftime('%b %d'))
        
        if active_habits_count > 0:
            completed_count = HabitLog.query.join(Habit).filter(
                Habit.user_id == current_user.id,
                HabitLog.date == date
            ).count()
            rate = (completed_count / active_habits_count) * 100
            timeline_rates.append(round(rate, 1))
        else:
            timeline_rates.append(0)

    # 2. Habit Performance Data
    habits = current_user.habits.all()
    habit_performance = []
    for habit in habits:
        logs_count = habit.logs.count()
        habit_performance.append({
            'name': habit.name,
            'completions': logs_count
        })
    
    # Sort by completions desc
    habit_performance = sorted(habit_performance, key=lambda x: x['completions'], reverse=True)[:5]

    # 3. Heatmap Data (Full History)
    heatmap_logs = []
    for habit in habits:
        logs = habit.logs.all()
        heatmap_logs.extend([log.date.isoformat() for log in logs])

    return jsonify({
        'timeline': {
            'labels': timeline_labels,
            'rates': timeline_rates
        },
        'performance': {
            'labels': [h['name'] for h in habit_performance],
            'data': [h['completions'] for h in habit_performance]
        },
        'heatmap': heatmap_logs
    })
