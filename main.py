from flask import Blueprint, render_template, url_for, request, redirect
from .anomalies import detect_anomaly,detect_anomaly_graph
import pandas as pd
import csv

main = Blueprint('main', __name__)

rows = [
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-05-01T00:00:00.000+03:00", "count": 4},
        {"time": "2015-06-01T00:00:00.000+03:00", "count": 0},
        {"time": "2015-07-01T00:00:00.000+03:00", "count": 0},
        ]


@main.route('/', methods=['POST','GET'])
def home():
    return render_template('base.html')

@main.route('/dashboard', methods= ['POST','GET'])
def dashboard():
    with open('/home/corey/Documents/data-leak/logs.csv','r') as f:
        reader = csv.DictReader(f,delimiter=';')
        # rows =[row for row in reader]
    return render_template('home.html',rows=rows)

@main.route('/detect-anomaly', methods=['POST','GET'])
def run_anomaly_detection():
    data = pd.read_csv('/home/corey/Documents/data-leak/logs.csv', parse_dates=['_time'])
    df = pd.DataFrame(data)
    detect_anomaly(df)
    return render_template('home.html',rows=rows)

@main.route('/graph')
def show_graph():
    data = pd.read_csv('/home/corey/Documents/data-leak/logs.csv', parse_dates=['_time'])
    df = pd.DataFrame(data)
    detect_anomaly_graph(data)
    return render_template('home.html', rows = rows)

if __name__ == '__main__':
    main.run(debug=True)