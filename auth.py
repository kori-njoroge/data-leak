from flask import Blueprint, render_template, url_for,redirect,flash
from sqlalchemy import create_engine, Column, Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import db_string
import bcrypt
import requests
import json

# creating a blueprint for auth file
auth= Blueprint('auth', __name__)

# create db engine
engine = create_engine(db_string)

# create db session
session = sessionmaker(bind=engine)
session = session()

# create the declarative base
Base = declarative_base()


@auth.route('/signup', methods=['POST','GET'])
def sign_up():
    # configuring bcrypt requirements
    salt = bcrypt.gensalt(rounds=8)
    if request.method == 'POST':
        # geting data from the html form
        email = request.form['email']
        username = request.form['username']
        role = request.form['role']
        password = request.form['password']

        # hashing the password
        hash = bcrypt.hashpw(password.encode('utf-8'), salt)

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
    return render_template("sign-up.html")

@auth.route('/login')
def login():
    username = request.form['username']
    password = request.form['password']

    user = session.query(User).filter_by(username = username)
    if user.count() > 0:
        user = user.first()
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            flash(f"Welcom {username}")
            return redirect(url_for('main.home'))
        else:
            flash('Wrong credentials')
    else:
        flash(f"User with username ({username}) not found")
    return render_template('login.html')