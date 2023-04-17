from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.utils import secure_filename

db = SQLAlchemy()

UPLOAD_FOLDER = 'website/static/upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # NOTE: if password is present : 'mysql://user:password@host/database'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/fgs_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api
    from .detect import detect

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(detect, url_prefix='/')

    from .models import User, Datasets

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app