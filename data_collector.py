import requests
import json
import redis

lines = ['bakerloo', 'central', 'circle', 'district', 'hammersmith-city', 'jubilee', 'metropolitan', 'northern',
         'piccadilly', 'victoria', 'waterloo-city']

# Configuration
API_ENDPOINT = 'https://api.tfl.gov.uk/Line/{}/Arrivals'
APP_ID = 'e2fe22dae03d4db0a54378c1a57a5438'
APP_KEY = 'a4ff3fc8cdc640cc8b3195435404ac03'

def fetch_and_update_data():
    headers = {
        'Accept': 'application/json',
        'App-ID': APP_ID,
        'App-Key': APP_KEY
    }

    unified_data = {}

    for line in lines:
        line_endpoint = API_ENDPOINT.format(line)
        response = requests.get(line_endpoint, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the API response to JSON format
            line_data = response.json()

            # Update the unified_data dictionary with line data
            unified_data[line] = line_data

        else:
            # Print an error message if the request failed
            print(f'Failed to fetch data for line: {line}')

    return unified_data

def store_data_in_redis(unified_data):
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    redis_key = 'RawLinesData'
    # Check if the key exists
    if r.exists('RawLinesData'):
        # Delete the existing data in the key
        r.delete('RawLinesData')

    # Convert the data to JSON string
    json_data = json.dumps(unified_data)

    # Set the JSON string as the value for the key
    r.set('RawLinesData', json_data)

    print(f'Raw data stored in Redis key: {redis_key}')

rawdata_to_publish = fetch_and_update_data()
store_data_in_redis(rawdata_to_publish)
