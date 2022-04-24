from googletrans import Translator
from flask_babel import _


def translate(text, source_language, dest_language='en'):
    translator = Translator()
    try:
        result = translator.translate(text, src=source_language, dest=dest_language)
    except ValueError:
        return _('Error: the translation service failed.')
    return result.text
