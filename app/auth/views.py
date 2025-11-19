from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response

auth_bp = Blueprint('auth', __name__, template_folder='templates')

VALID_USERNAME = "user1"
VALID_PASSWORD = "secret"

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if session.get('user'):
        flash("Ви вже увійшли.", "info")
        return redirect(url_for('auth.profile'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username
            flash("Успішний вхід.", "success")
            return redirect(url_for('auth.profile'))
        else:
            flash("Невірні дані.", "danger")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("Ви вийшли.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET','POST'])
def profile():
    user = session.get('user')
    if not user:
        flash("Будь ласка, увійдіть.", "warning")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        action = request.form.get('action')
        resp = make_response(redirect(url_for('auth.profile')))
        if action == 'add_cookie':
            key = request.form.get('cookie_key','').strip()
            value = request.form.get('cookie_value','')
            days = int(request.form.get('cookie_term_days','7') or 0)
            if key:
                resp.set_cookie(key, value, max_age=days*24*3600)
                flash(f"Кука {key} додана.", "success")
            else:
                flash("Ключ не може бути пустим.", "danger")
            return resp
        if action == 'delete_cookie':
            key = request.form.get('delete_key','').strip()
            if key:
                resp.set_cookie(key, '', max_age=0)
                flash(f"Кука {key} видалена.", "success")
            else:
                flash("Вкажіть ключ для видалення.", "danger")
            return resp
        if action == 'delete_all':
            resp = make_response(redirect(url_for('auth.profile')))
            for k in request.cookies.keys():
                resp.set_cookie(k, '', max_age=0)
            flash("Видалено всі кукі.", "success")
            return resp

    return render_template('auth/profile.html', user=user, cookies=request.cookies, scheme=request.cookies.get('scheme','light'))

@auth_bp.route('/set_scheme/<scheme>')
def set_scheme(scheme):
    if not session.get('user'):
        flash("Будь ласка, увійдіть.", "warning")
        return redirect(url_for('auth.login'))
    resp = make_response(redirect(url_for('auth.profile')))
    resp.set_cookie('scheme', scheme, max_age=30*24*3600)
    flash(f"Схема: {scheme}", "success")
    return resp
