from datetime import datetime

from app import db
from app.main import blueprint
from app.main.forms import PostForm, EditProfileForm
from app.models import Post, User, Person
from app.translate import translate
from flask import g, flash, url_for, request, current_app, render_template, jsonify
from flask_babel import get_locale, _
from flask_login import current_user, login_required
from langdetect import detect, LangDetectException
from werkzeug.utils import redirect


@blueprint.before_request
def before_request():
    # обновляем время последнего пребывания пользователя
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    # предпочтительный язык пользователя
    g.locale = str(get_locale())


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        # пытаемся определить язык поста. Если он не определен, то оставляем пустую строку
        try:
            language = detect(form.post.data)
        except LangDetectException:
            language = ''

        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))

    # текущее страница постов
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    persons = db.session.query(Person).all()

    for person in persons:
        print(person.face)

    params = {
        "title": _('Home'),
        'persons': persons,
        'form': form,
        'posts': posts.items,
        "next_url": next_url,
        "prev_url": prev_url
    }
    return render_template('main/index.html', **params)


@blueprint.route('/user/<username>')
@login_required
def user(username):
    # находим пользователя под именем username или вызываем ошибку 404
    user = db.session.query(User).filter(User.username == username).first_or_404()

    # навигация по постам
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    params = {
        "user": user,
        "posts": posts.items,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render_template('main/user.html', **params)


@blueprint.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.user', username=current_user.username))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    params = {
        "title": _('Edit Profile'),
        "form": form
    }
    return render_template('main/edit_profile.html', **params)


@blueprint.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})
