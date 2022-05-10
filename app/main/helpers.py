import os
import secrets

from PIL import Image
from flask import current_app
from langdetect import detect, LangDetectException


def lang_detect(text):
    try:
        language = detect(text)
    except LangDetectException:
        language = ''
    return language


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['AVATARS_PATH'], picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn
