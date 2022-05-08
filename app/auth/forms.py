from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_babel import _, lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('Пайдаланушы аты'), validators=[DataRequired()])
    password = PasswordField(_l('Құпиясөз'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Есте сақтау'))
    submit = SubmitField(_l('Кіру'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Пайдаланушы аты'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Құпиясөз'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Құпиясөзді қайта теріңіз'), validators=[DataRequired(),
                                           EqualTo('Құпиясөз')])
    submit = SubmitField(_l('Тіркелу'))

    def validate_username(self, username):
        user = db.session.query(User).filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError(_('Басқа пайдаланушы атын таңдаңыз'))

    def validate_email(self, email):
        user = db.session.query(User).filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError(_('Басқа email таңдаңыз'))
