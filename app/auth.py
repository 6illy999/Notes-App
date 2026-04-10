from flask import Blueprint, render_template, flash, redirect, url_for,request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit


bp = Blueprint('auth', __name__)


# Login route
@bp.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='error')
            return redirect(url_for('auth.login')) 
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in', category='success')

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('routes.home')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)



# Logout route
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Registration route
@bp.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if len(form.username.data) < 4:
            flash('Username too short', category='error')
        elif len(form.password.data) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('You are now registered', category='success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', title='Sign Up', form=form)