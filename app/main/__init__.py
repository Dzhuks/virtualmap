from flask import Blueprint


blueprint = Blueprint(
    "main",
    __name__,
    template_folder="templates"
)

from app.main import routes, forms