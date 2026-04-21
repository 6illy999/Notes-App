from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager
import app

db = SQLAlchemy()
DB_NAME = "database.db"

migrate = Migrate()

login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asecretkeystring'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['POSTS_PER_PAGE']  = 5
    db.init_app(app)

    migrate.init_app(app, db)

    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/')

    from app import models

    #create_database(app)

    return app

'''
def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
'''