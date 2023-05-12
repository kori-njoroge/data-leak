from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import db_string
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:MyPass@localhost:3306/dataleakDB"
    app.config['SECRET_KEY']= os.environ.get('SECRET_KEY')
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app