from flask import Flask
from flask import Blueprint, render_template

crud = Blueprint("crud",__name__, template_folder="template", static_folder="static")

@crud.route("/")
def index():
    return render_template("crud/index.html")


def create_app():
    app=Flask(__name__)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
