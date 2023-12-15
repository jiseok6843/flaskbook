from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#create_app함수 생성
def create_app():

    # 플라스크 인스턴스(객체)를 생성
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="googleCloudPlatform",
        SQLALCHEMY_DATABASE_URI=
        f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True, 
        #WTF_CSRF_SECRET_KEY="sadasdsdasde32324dfg",
    )

    db.init_app(app)
    Migrate(app, db)


    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app


