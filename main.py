from flask import Blueprint, render_template, url_for, request, redirect

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')

# @main.route('/home')
# def home():
#     return 'home'

if __name__ == '__main__':
    main.run(debug=True)