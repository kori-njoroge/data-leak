from flask import Blueprint, render_template, url_for

auth= Blueprint('auth', __name__)

@auth.route('/signup')
def sign_up():
    return render_template("sign-up.html")

@auth.route('/login')
def login():
    return render_template('login.html')