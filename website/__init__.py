from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    # NOTE: if password is present : 'mysql://user:password@host/database'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/fgs_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
    db.init_app(app)

    from .views import views
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    from .models import User

    return app