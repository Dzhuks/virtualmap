from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length

from app import db
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Пайдаланушы аты'), validators=[DataRequired()])
    about_me = TextAreaField(_l('Мен туралы'), validators=[Length(min=0, max=140)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(_l('Өзгерту'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.query(User).filter(User.username == self.username.data).first()
            if user is not None:
                raise ValidationError(_('Басқа пайдаланушы атын таңдаңыз'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Пікір қалдырыңыз'), validators=[DataRequired()])
    submit = SubmitField(_l('Жүктеу'))
