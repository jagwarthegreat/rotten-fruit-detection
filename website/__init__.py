from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app