from flask import Blueprint, render_template, url_for,redirect,flash,request
from sqlalchemy import create_engine, Column, Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import bcrypt
import re
# import easygui
import os
import random
import string

from . import db

# mail imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .config import db_string
from .models.user import User
from .models.comment import Comment

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


# welcome email function
def send_email_notification_register(email, username):
    # Set up email notification
    from_address = os.environ.get('MAILER_EMAIL')
    to_address = email
    subject = 'Welcome!'
    message = f'Welcome {username}!, to Weling data leak detection system. We are happy you could join us.Here at Weling your data security is our priority'
    
    # Send email
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address,os.environ.get('MAILER_PWD'))
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()


@auth.route('/signup', methods=['POST','GET'])
def sign_up():
    session.rollback()
    password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"
    # configuring bcrypt requirements
    salt = bcrypt.gensalt(rounds=8)
    if request.method == 'POST':
        # geting data from the html form
        email = request.form['email']
        username = request.form['username']
        role = request.form['role']
        password = request.form['password']
        conpassword = request.form['confpass']
        
        if not re.match(password_pattern, password):
            message=["Weak password, Try again"]
            return render_template('sign-up.html',message=message)
        else:
            # hashing the password
            if password == conpassword :
                hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            user = session.query(User).filter_by(email = email)
            if user.count() > 0:
                message = ["User with the Email already exists"]
                return render_template('sign-up.html',message=message)
            else:
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
                send_email_notification_register(email,username)
                return redirect(url_for('auth.login'))
    mess=['Password must:  Include a special character',
    'More than 8 characters long',
    'Include a capital and small letters']
    return render_template("sign-up.html", message=mess)

@auth.route('/login', methods=['POST','GET'])
def login():
    # flash('Welcome to Login')
    return render_template('login.html')

@auth.route('/logvalidate', methods=['POST','GEt'])
def login_validate():
    username = request.form['username']
    password = request.form['password']

    user = session.query(User).filter_by(username = username)
    if user.count() > 0:
        user = user.first()
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            code = generate_random_string()
            email= user.email
            subject ='Login OTP'
            send_code_to_user(email,code,subject)
            # store code
            message = update_approved(email,code)
            url ='verify'
            return render_template('enter-code.html',email=email, message = message, url=url)
        else:
            message= 'Wrong credentials'
            return render_template('login.html', message= message)
    else:
        message= 'User not found'
        return render_template('login.html', message= message)

# Logout route
@auth.route('/logout', methods=['GET'])
def logout():
    # session.pop('logged_in', None)
    return redirect(url_for('auth.login'))


# forgot password section
@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')

@auth.route('/send-code',methods=['POST'])
def send_code():
    # getting email
    email= request.form['email']

    # generate and send code to the user
    code=generate_random_string()
    # save code
    message =update_approved(email, code)
    if message == 'User not found':
        return render_template('forgot.html', message =message)
    else:
        # send mail
        subject = 'Forgot Password!'
        send_code_to_user(email, code, subject)
        url= 'verify-code'
        return render_template('enter-code.html',email =email, message = message, url=url)

@auth.route('/verify-code', methods=['POST'])
def verfify():
    user_code= request.form['code']
    email = request.form['email']
    # query code from db
    stored_code = get_code(email)

    # compare the codes
    if user_code == stored_code:
        return render_template('reset-password.html', email=email)
    else:
        message = 'Wrong verfification code try again'
        return render_template('enter-code.html', email = email, message=message)


# verify on login
@auth.route('/verify', methods=['POST','GET'])
def verfify_login():
    user_code= request.form['code']
    email = request.form['email']
    # query code from db
    stored_code = get_code(email)

    # compare the codes
    if user_code == stored_code:
        return redirect(url_for('main.dashboard'))
    else:
        message = 'Wrong verfification code try again'
        return render_template('enter-code.html', email = email, message=message)


# generate random code
def generate_random_string():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(6))
    return code

# store code in db
def update_approved(email,code):
    user = session.query(User).filter_by(email = email).first()
    message =''
    if user:
        user.approved = code
        session.commit()
        message = 'Code has been sent'
    else:
        print("User not found.")
        message = 'User not found'
    return message


def send_code_to_user(email, code, subject):
    # Set up email notification
    from_address = os.environ.get('MAILER_EMAIL')
    to_address = email
    subject = subject
    message = f'Please enter this code to the web page when requested. Your code is ({code})'
    
    # Send email
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address,os.environ.get('MAILER_PWD'))
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()

# get stored code
def get_code(email):
    # user = session.query(User).filter_by(email=email).first()
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user.approved
    else:
        return None

# reset password route
@auth.route('/reset-password', methods=['POST','GET'])
def reset_pass():
    password= request.form['password']
    confPass = request.form['confpassword']
    email=request.form['email']

    if password == confPass:
        user = session.query(User).filter_by(email=email).first()   
        if user: 
            # generate salt
            salt = bcrypt.gensalt(rounds=8)
            # hashing the password
            hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            # send to db
            user.password = hash
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            message = 'User not found'
            return render_template('change-pass.html', message=message)

@auth.route('/change-password', methods=['POST', 'GET'])
def change_pass():
    if request.method == 'POST':
        email=request.form['email']
        password= request.form['password']
        confPass = request.form['confpassword']

        if password == confPass:
            user = session.query(User).filter_by(email=email).first()
            if user:
                # generate salf
                salt = bcrypt.gensalt(rounds=8)
                # hashing the password
                hash = bcrypt.hashpw(password.encode('utf-8'), salt)
                # send to db
                user.password = hash
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                message= 'User not found'
                return render_template('change-pass.html', message=message)

        else:
            message= 'Passwords do not match'
            return render_template('change-pass.html', message=message)
    return render_template('change-pass.html')

@auth.route('/contact')
def contact():
    return render_template('contact.html')
@auth.route('/comment', methods=['POST','GET'])
def comment():
    session.rollback()
    contact= request.form['email']
    comments = request.form['comment']
    # comment object
    comment = Comment(
        contact = contact ,
        comment =comments
    )
    # add new use to db
    session.add(comment)
    message="Message received we'll get back to your shortly"
    session.commit()
    return render_template('contact.html', message=message)