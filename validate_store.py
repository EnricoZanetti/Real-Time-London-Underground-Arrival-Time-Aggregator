import json
import psycopg2
import datetime
import redis

def clean_json(json_data):
    cleaned_json_str = json.dumps(json_data, indent=4)
    return cleaned_json_str

def structure_validate_data(data):
    main_data = json.loads(data)

    prediction_list = []  # Create a list to store prediction data
    for line, predictions in main_data.items():
        for prediction in predictions:
            prediction_data = {}
            prediction_data['vehicleId'] = prediction.get('vehicleId', None)
            prediction_data['currentLocation'] = prediction.get('currentLocation', None)
            prediction_data['destinationName'] = prediction.get('destinationName', None)
            prediction_data['lineName'] = prediction.get('lineName', None)

            # Format the expected arrival date and time
            expected_arrival = datetime.datetime.strptime(prediction.get('expectedArrival', None), "%Y-%m-%dT%H:%M:%SZ")
            prediction_data['expectedArrival'] = expected_arrival.strftime("Date: %Y-%m-%d, Time: %H:%M:%S")

            prediction_data['platformName'] = prediction.get('platformName', None)
            prediction_data['stationName'] = prediction.get('stationName', None)

            # Convert timeToStation to minutes and seconds
            time_to_station = prediction.get('timeToStation', None)
            minutes = time_to_station // 60
            seconds = time_to_station % 60

            prediction_data['timeToStation'] = f"{minutes} minutes and {seconds} seconds"
            prediction_data['towards'] = prediction.get('towards', None)

            prediction_list.append(prediction_data)  # Append each prediction data to the list

    return prediction_list

def retrieve_raw_data(redis_client, redis_key):
    raw_data = redis_client.get(redis_key)
    if raw_data is not None:
        return raw_data.decode('utf-8')
    return None

def store_clean_data(redis_client, redis_key, pred_clean_list):
    # Check if the key exists
    if redis_client.exists(redis_key):
        # Delete the existing data in the key
        redis_client.delete(redis_key)

    # Convert the data to JSON string
    json_data = json.dumps(pred_clean_list, indent=4)

    # Set the JSON string as the value for the key
    redis_client.set(redis_key, json_data)

    print(f'Clean data stored in Redis key: {redis_key}')


def transfer_data_to_postgresql(pred_clean_list, connection):
    cursor = connection.cursor()
    try:
        for prediction in pred_clean_list:
            cursor.execute(
                "INSERT INTO lines (vehicleId, currentLocation, destinationName, lineName, expectedArrival, platformName, stationName, timeToStation, towards) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (prediction['vehicleId'], prediction['currentLocation'], prediction['destinationName'], prediction['lineName'], prediction['expectedArrival'], prediction['platformName'], prediction['stationName'], prediction['timeToStation'], prediction['towards']))

        connection.commit()
        print("Data transferred to PostgreSQL successfully!")
    except Exception as e:
        print("Error transferring data to PostgreSQL:", str(e))
    cursor.close()

def execution():
    # PostgreSQL
    connection = psycopg2.connect(
        host="localhost",
        port="5433",
        database="tubedb",
        user="team06",
        password="bdt2023_06"
    )

    # Redis
    redis_client = redis.Redis(host='localhost', port=6379)

    # Read data from Redis key 'raw_unified_data'
    raw_data = retrieve_raw_data(redis_client, 'RawLinesData')

    if raw_data is None:
        print('No raw data found in Redis. Make sure to store the raw data in the Redis key.')
        return

    # Process the raw data
    pred_clean_list = structure_validate_data(raw_data)

    # Store clean data in Redis key 'CleanLinesData'
    store_clean_data(redis_client, 'CleanLinesData', pred_clean_list)

    # Store data into tubedb database
    transfer_data_to_postgresql(pred_clean_list, connection)

    connection.close()

execution()
