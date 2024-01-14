from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email_address=email_address).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.todos'))
            else:
                flash('Ooops! Something went wrong!', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email_address = request.form.get('email_addresss')
        password = request.form.get('password')

        user = User.query.filter_by(email_address=email_address).first()
        if user:
            flash('Sorry! That email has already been taken!', category='error')
        elif len(first_name) < 1:
            flash('First name must be more than one character', category='error')
        elif len(last_name) < 1:
            flash('Last name must be more than one character', category='error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters', category='error')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email_address=email_address, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Your account has been created! You can now login', category='success')
            return redirect(url_for('auth.login'))
    return render_template("signup.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))