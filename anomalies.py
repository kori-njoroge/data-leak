import pandas as pd
import statsmodels.graphics.api as smg
import statsmodels.graphics.tsaplots as sgt
import statsmodels.graphics.regressionplots as sgr
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import statsmodels.api as sm
import statsmodels.graphics.tsaplots as sgt
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import pygame
from playsound import playsound
import time


load_dotenv()

def detect_anomaly(data):
    # Set up the SPC chart
    count = 'Count of 1682446202.21'
    # Calculate the mean and standard deviation of the data
    mean = data[count].mean()
    std_dev = data[count].std()

    # Calculate the upper and lower control limits
    ucl = mean + 3 * std_dev
    lcl = mean - 3 * std_dev

    control_limits = (lcl,ucl)

    # Create the SPC chart
    fig, ax = plt.subplots()
    ax.plot(data[count], 'bo-', markersize=4)
    ax.axhline(y=mean, color='r', linestyle='--', linewidth=1, label='Mean')
    ax.axhline(y=ucl, color='g', linestyle='--', linewidth=1, label='UCL')
    ax.axhline(y=lcl, color='g', linestyle='--', linewidth=1, label='LCL')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel(count)
    ax.legend()
    plt.show()

    # Detect anomalies
    anomalies = []
    for i, row in data.iterrows():
        if row[count] > control_limits[1] or row[count] < control_limits[0]:
            anomalies.append(row)
    
    # Send notification
    if len(anomalies) > 0:
        send_email_notification(anomalies)


def send_email_notification(anomalies):
    # Set up email notification
    from_address = os.environ.get('MAILER_EMAIL')
    to_address = 'Welburling@gmail.com'
    subject = 'Anomaly detected'
    message = 'Anomalies were detected at the following times:\n\n'
    
    for anomaly in anomalies:
        Time = '_time'
        Value = 'Count of 1682446202.21'
        message += f"{anomaly[Time].strftime('%Y-%m-%d %H:%M:%S')}: {anomaly[Value]}\n"
    
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

    # pygame alert
    pygame.init()
    # pygame.mixer.music.load('/home/welbur/Documents/data-leak/alert.mp3')
    pygame.mixer.music.load('/home/corey/Documents/data-leak/alert.mp3')
    pygame.mixer.music.play()
    time.sleep(4)
    pygame.mixer.music.stop()


def detect_anomaly_graph(data):
    # Set up the SPC chart
    count = 'Count of 1682446202.21'
    # Calculate the mean and standard deviation of the data
    mean = data[count].mean()
    std_dev = data[count].std()

    # Calculate the upper and lower control limits
    ucl = mean + 3 * std_dev
    lcl = mean - 3 * std_dev

    control_limits = (lcl,ucl)

    # Create the SPC chart
    fig, ax = plt.subplots()
    ax.plot(data[count], 'bo-', markersize=4)
    ax.axhline(y=mean, color='r', linestyle='--', linewidth=1, label='Mean')
    ax.axhline(y=ucl, color='g', linestyle='--', linewidth=1, label='UCL')
    ax.axhline(y=lcl, color='g', linestyle='--', linewidth=1, label='LCL')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel(count)
    ax.legend()
    plt.show()
