import json
from flask import Flask, render_template, request, redirect
import redis

def get_line_arrivals(line_name, redis_client, redis_key):
    clean_data = redis_client.get(redis_key)
    if clean_data is not None:
        arrivals = json.loads(clean_data)
        line_arrivals = []

        for arrival in arrivals:
            if arrival["lineName"] == line_name:
                arrival_info = {
                    "vehicleId": arrival["vehicleId"],
                    "currentLocation": arrival["currentLocation"],
                    "destinationName": arrival["destinationName"],
                    "expectedArrival": arrival["expectedArrival"],
                    "platformName": arrival["platformName"],
                    "stationName": arrival["stationName"],
                    "TimeToStation": arrival["timeToStation"],
                    "Towards": arrival["towards"]
                }

                line_arrivals.append(arrival_info)

        return line_arrivals

    else:
        print("Clean data not found in Redis.")
        return None


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index3.html")


@app.route("/results")
def show_results():
    line_name = request.args.get("line_name")

    # Redis
    redis_client = redis.Redis(host='localhost', port=6379)
    redis_key = 'CleanLinesData'

    line_arrivals = get_line_arrivals(line_name, redis_client, redis_key)

    if line_arrivals is not None:
        return render_template("results3.html", line_arrivals=line_arrivals, LS=line_name)
    else:
        return render_template("error.html", message="Clean data not found in Redis.")

    return redirect("/")

if __name__ == "__main__":
    app.run()
