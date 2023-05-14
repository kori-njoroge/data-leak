from flask import Flask, render_template
from splunklib import client
import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW
from scipy.stats import norm
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

app = Flask(__name__)


# Splunk settings
HOST = 'localhost'
PORT = 8000
USERNAME = 'admin'
PASSWORD = os.environ.get('SPLUNKPWD')
APP_NAME = 'search'

# SPC chart settings
CONTROL_LIMITS = 3
SIGMA = 2
SUBGROUP_SIZE = 5

@app.route('/')
def home():
    # Connect to Splunk
    service = client.connect(
        host=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        app=APP_NAME,
        verify=False
    )

    print("connected")
    # Search for data
    search_query = 'search index=myindex | stats count by _time'
    job = service.jobs.create(search_query)
    while not job.is_done():
        pass
    results = job.results()

    # Convert results to Pandas DataFrame
    data = []
    for result in results:
        row = {}
        for key, value in result.items():
            row[key] = value
        data.append(row)
    df = pd.DataFrame(data)

    # Calculate control limits and detect anomalies
    df['_time'] = pd.to_datetime(df['_time'])
    subgrouped_data = df.groupby(pd.Grouper(key='_time', freq='D')).agg({'count': lambda x: list(x)})
    subgrouped_data['subgroup_mean'] = subgrouped_data['count'].apply(lambda x: np.mean(x))
    subgrouped_data['subgroup_std'] = subgrouped_data['count'].apply(lambda x: np.std(x))
    subgrouped_data['upper_control_limit'] = subgrouped_data['subgroup_mean'] + CONTROL_LIMITS * subgrouped_data['subgroup_std']
    subgrouped_data['lower_control_limit'] = subgrouped_data['subgroup_mean'] - CONTROL_LIMITS * subgrouped_data['subgroup_std']
    subgrouped_data['anomaly'] = np.nan
    for index, row in subgrouped_data.iterrows():
        subgroup_stats = DescrStatsW(row['count'], weights=np.ones(len(row['count'])) / len(row['count']))
        subgroup_mean = subgroup_stats.mean
        subgroup_std = subgroup_stats.std
        for i, count in enumerate(row['count']):
            if count > row['upper_control_limit'][i] or count < row['lower_control_limit'][i]:
                row['anomaly'][i] = True

    # Generate alert if anomalies detected
    if subgrouped_data['anomaly'].any():
        # Send alert to admin
        print('Anomalies detected!')

    # Render template with SPC chart
    return render_template('index.html', data=subgrouped_data.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
