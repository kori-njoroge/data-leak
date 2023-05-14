from flask import Blueprint, render_template, url_for, request, redirect,flash
from .anomalies import detect_anomaly
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('base.html')

@main.route('/dashboard')
def dashboard():
    return 'home'

@main.route('/detect-anomaly', methods=['POST','GET'])
def run_anomaly_detection():
    # data = request.json
    data = pd.read_csv('/home/corey/Documents/data-leak/logs.csv', parse_dates=['_time'])
    df = pd.DataFrame(data)
    detect_anomaly(df)
    return 'Anomaly detection completed'


if __name__ == '__main__':
    main.run(debug=True)