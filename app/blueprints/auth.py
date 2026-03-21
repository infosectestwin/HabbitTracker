import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, oauth
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorize')
def google_authorize():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        flash(f'OAuth error: {str(e)}')
        return redirect(url_for('auth.login'))
        
    user_info = token.get('userinfo')
    if not user_info:
        flash('Failed to fetch user information from Google.')
        return redirect(url_for('auth.login'))
    
    email = user_info.get('email')
    if not user_info.get('email_verified'):
        flash('Google email not verified.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        # Create a new user if it doesn't exist
        import secrets
        username = user_info.get('name') or email.split('@')[0]
        user = User(username=username, email=email)
        user.set_password(secrets.token_hex(16))
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('main.index'))

def is_password_strong(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Login using email now
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=request.form.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email address already registered')
            return redirect(url_for('auth.register'))

        # Password strength check
        is_strong, message = is_password_strong(password)
        if not is_strong:
            flash(message)
            return redirect(url_for('auth.register'))
            
        # Use email as username since we removed it from UI
        user = User(username=email, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
