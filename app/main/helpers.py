from langdetect import detect, LangDetectException


def lang_detect(text):
    try:
        language = detect(text)
    except LangDetectException:
        language = ''
    return language
