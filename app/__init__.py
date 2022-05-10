import logging
import os
from logging.handlers import RotatingFileHandler

from app.extensions import db
from config import Config
from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment

migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Бұл парақшаға кіру керек.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


# функция для создания app для более удобного тестирования
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import blueprint as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import blueprint as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import blueprint as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


# функция возвращающая самый предпочтительный язык для пользователя из списка подерживаемых языков
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models
