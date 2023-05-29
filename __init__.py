from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import db_string
from dotenv import load_dotenv
import os
import ssl

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:MyPass@localhost:3306/dataleakDB"
    # app.config['SECRET_KEY']= os.environ.get('SECRET_KEY','os.environ.getisverfysjhshdjksjkdfjksaiuguwemabsjkdgouwgefew')
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from .config import db_string
# from dotenv import load_dotenv
# import os
# import ssl

# load_dotenv()
# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:MyPass@localhost:3306/dataleakDB"

#     # SSL Configuration
#     app.config['SERVER_NAME'] = '127.0.0.1'  # Replace with your domain or hostname
#     app.config['SSL_CERTIFICATE'] = './ssl/certificate.pem'  # Updated to the PEM file
#     app.config['SSL_PRIVATE_KEY'] = './ssl/private.pem'  # Updated to the PEM file

#     db.init_app(app)

#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)

#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)

#     return app

# app = create_app()

# # if __name__ == '__main__':
# #     # Run the Flask application with SSL enabled
# #     app.run(ssl_context=('./ssl/certificate.pem', './ssl/private.pem'))
