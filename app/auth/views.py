from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from ..forms import LoginForm
from app.users.models import User
from sqlalchemy import or_, select
from ..forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from app import db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("Ви вже увійшли.", "info")
        return redirect(url_for('auth.account')) #return redirect(url_for('auth.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Реєстрація пройшла успішно.", "success")
        return redirect(url_for('auth.account')) #return redirect(url_for('auth.profile'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Ви вже увійшли.", "info")
        return redirect(url_for('auth.account')) #return redirect(url_for('auth.profile'))
    
    form = LoginForm()

    if form.validate_on_submit():
        identifier = form.username.data.strip()
        user = db.session.scalar(select(User).where(or_(User.username == identifier, User.email == identifier)))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Успішний вхід.", "success")
            return redirect(url_for('auth.account')) #return redirect(url_for('auth.profile'))
        flash("Невірні дані.", "danger")

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ви вийшли.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route("/account")
@login_required
def account():
    return render_template('auth/account.html', user=current_user)

@auth_bp.route("/all")
@login_required
def all_users():
    users = db.session.scalars(select(User).order_by(User.id)).all()
    count = len(users)
    return render_template("auth/all_users.html", users=users, count=count)

@auth_bp.route('/set_scheme/<scheme>')
@login_required
def set_scheme(scheme):
    resp = make_response(redirect(url_for('auth.profile')))
    resp.set_cookie('scheme', scheme, max_age=30*24*3600)
    flash(f"Схема: {scheme}", "success")
    return resp
