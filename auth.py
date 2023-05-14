from flask import Blueprint, render_template, url_for,redirect,flash,request
from sqlalchemy import create_engine, Column, Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import bcrypt
import easygui
import os

# mail imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .config import db_string
from .models.user import User

load_dotenv()
# creating a blueprint for auth file
auth= Blueprint('auth', __name__)

# create db engine
engine = create_engine(db_string)

# create db session
session = sessionmaker(bind=engine)
session = session()

# create the declarative base
Base = declarative_base()

# EMAIL SENDER CONFIGURATIONS
# SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587  
smtp_username = os.environ.get('EMAIL')
smtp_password = os.environ.get('EMAILPWD')


@auth.route('/signup', methods=['POST','GET'])
def sign_up():
    session.rollback()
    # configuring bcrypt requirements
    salt = bcrypt.gensalt(rounds=8)
    if request.method == 'POST':
        # geting data from the html form
        email = request.form['email']
        username = request.form['username']
        role = request.form['role']
        password = request.form['password']
        conpassword = request.form['confpass']

        # hashing the password
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        if password == conpassword :
            # create a user object
            user = User(
                email = email,
                username =username,
                role = role,
                password = hash
            )

            # add new use to db
            session.add(user)
            session.commit()
            return redirect(url_for('auth.login'))
        else:
            easygui.msgbox('Passwords do not match')
    return render_template("sign-up.html")

@auth.route('/login', methods=['POST','GET'])
def login():
    flash('Welcome to Login')
    return render_template('login.html')

@auth.route('/logvalidate', methods=['POST','GEt'])
def login_validate():
    username = request.form['username']
    password = request.form['password']

    user = session.query(User).filter_by(username = username)
    if user.count() > 0:
        user = user.first()
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            easygui.msgbox(f"Welcome {username}")
            # session['logged_in'] = True
            return redirect(url_for('main.dashboard'))
        else:
            flash('Wrong credentials')
            easygui.msgbox('Wrong credentials')
    else:
        flash(f"User with username ({username}) not found")
    return render_template('login.html')

# Logout route
@auth.route('/logout', methods=['GET'])
def logout():
    # session.pop('logged_in', None)
    return redirect(url_for('auth.login'))