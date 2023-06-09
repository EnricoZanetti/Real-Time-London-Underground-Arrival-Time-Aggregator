import time
from data_collector import fetch_and_update_data
from data_collector import store_data_in_redis
from validate_store import execution

if __name__ == '__main__':
    while True:
        print("-" * 50 , "London Underground: Collecting Live Data on Arrivals", "-" * 50 )
        rawdata_to_publish = fetch_and_update_data()
        store_data_in_redis(rawdata_to_publish)
        execution()
        time.sleep(30)  # Sleep for 30 seconds before fetching and updating data again
