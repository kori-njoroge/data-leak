import splunklib.client as client

# Set up connection parameters
host = 'localhost'
port = 8089
username = 'admin'
password = '@Splunk1'

# Create a Service object to connect to Splunk
service = client.connect(
    host=host,
    port=port,
    username=username,
    password=password
)

# Check if the connection was successful
if service:
    print("Connected to Splunk!")
else:
    print("Connection to Splunk failed.")

# Query for data
# Define your search query
search_query = 'search index=main | head 10'

# Output format
search_kwargs = {
    'output_mode': 'csv',  # Specify CSV as the output format
    'earliest_time': '-24h',  # Set the earliest time for the search
    'latest_time': 'now'  # Set the latest time for the search
}

# Execute the search query
job = service.jobs.create(search_query, **search_kwargs)

# Wait for the search job to finish
while not job.is_done():
    pass

# Get the search results
search_results = job.results()

# Process and extract the data from the search results
# for result in search_results:
#     # Process each event or log record
#     print(result)

# Clean up the search job
job.cancel()
