from app import db
from app.auth import blueprint
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from flask import url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
from flask_babel import _


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # если пользователь уже зарегестрирован, то он перенаправляется в main.index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Тіркелу сәтті өтті!'))
        return redirect(url_for('auth.login'))
    
    params = {
        "title": _('Тіркелу'),
        "form": form
    }
    return render_template('auth/register.html', **params)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Пайдаланушы жүйеде табылмады немесе құпиясөз қате терілді"))
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)

        """
        * Если URL-адрес входа не включает аргумент next, пользователь перенаправляется на индексную страницу. 
        * Если URL-адрес входа включает аргумент next, который установлен на URL-адрес другого сайта, то пользователь 
        перенаправляется на индексную страницу. 
        * Если URL-адрес входа включает аргумент next, который установлен в 
        относительный путь, то есть на самом сайте, то тогда пользователь перенаправляется на этот URL-адрес. 
        """
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    params = {
        "title": _('Кіру'),
        "form": form
    }
    return render_template('auth/login.html', **params)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
