from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configuration from environment variable
    app.config['SECRET_KEY'] = 'DB_CONNECTION_STRING'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:securityapp@securityapp.czp1fr3ynvvj.ap-south-1.rds.amazonaws.com/security_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, emp

    with app.app_context():
      db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
      return User.query.get(int(id))

    return app