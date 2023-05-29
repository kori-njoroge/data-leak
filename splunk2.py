from __future__ import print_function
import splunklib.client as client
import sys
import os
import csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import splunklib.results as results



HOST = "localhost"
PORT = 8089
USERNAME = "admin"
PASSWORD = "@Splunk1"

service = client.connect(
    host=HOST,
    port=PORT, 
    username=USERNAME,
    password=PASSWORD)

rr = results.ResultsReader(service.jobs.export("search index=main earliest=-24h | tail 100"))
# print(rr)

# Define the path and filename for the CSV file
csv_file_path = "search_results.csv"

# Open the CSV file in write mode
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    for result in rr:
        if isinstance(result, results.Message):
            # Diagnostic messages might be returned in the results
            print('%s: %s' % (result.type, result.message))
        elif isinstance(result, dict):
            # Normal events are returned as dicts
            writer.writerow(result.values())

assert rr.is_preview == False