import requests
import json
import influxdb_client

def getVzloggerValues(config):
    measurement_points = []

    #get config
    debug_output = config["global"]["debug_output"]
    hostname = config["vzlogger"]["hostname"]
    measurement = config["vzlogger"]["measurement"]
    channels = config["vzlogger"]["channels"]

    for channel in channels:
        channel_uuid = channel['uuid']
        channel_name = channel['name']

        try:
            #get data from vzlogger
            url = requests.get("http://" + hostname + "/" + channel_uuid, timeout=10)

            try:
                #parse data
                json_data = json.loads(url.text)
                total_kWh = round(json_data['data'][0]['tuples'][0][1] / 1000, 4)
                point = influxdb_client.Point(measurement).tag("channel", channel_name).tag("value", "total").field("kWh", total_kWh)
                measurement_points.append(point)
                if debug_output == "true":
                    print(channel_name+": " + str(total_kWh) + " kWh")

            except:
                if debug_output == "true":
                    print("Failed to parse vzlogger data.")

        except:
            if debug_output == "true":
                print("Failed to get vzlogger data. Is server offline?")

    return measurement_points
