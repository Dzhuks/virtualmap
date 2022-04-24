import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            """
            Команда extract извлекает сообщения из исходных файлов и создавает POT-файл
            """
            raise RuntimeError('extract command failed')
        if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
            """
            Команда pybabel init принимает файл messages.pot в качестве входных данных и создает новый каталог 
            для определенного языка, указанного в параметре -l в каталог, указанный в параметре -d
            (по умолчанию Flask-Babel будет искать файлы перевода в директорий translations)
            """
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            """
            Команда extract извлекает сообщения из исходных файлов и создавает POT-файл
            """
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            """
            Команда update принимает новый файл messages.pot и объединяет его во все файлы messages.po, связанные с проектом
            """
            raise RuntimeError('update command failed')
        """
        Программа удаляет messages.pot файл, так как этот файл может быть легко регенерирован при необходимости еще раз.
        """
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            """
            Команда compile добавляет файл messages.mo рядом с messages.po в каждом языковом репозитории. 
            Файл .mo — это файл, который Flask-Babel будет использовать для загрузки переводов в приложение.
            """
            raise RuntimeError('compile command failed')
