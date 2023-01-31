import requests
import json
import influxdb_client
from inverter import getInverterValues
from vzlogger import getVzloggerValues
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    config_file = open("config.json")
    config = json.load(config_file)

    debug_output = config["global"]["debug_output"]
    inverter_enabled = config["inverter"]["enabled"]
    vzlogger_enabled = config["vzlogger"]["enabled"]
    influx_url = config["influx"]["url"]
    influx_org = config["influx"]["org"]
    influx_bucket = config["influx"]["bucket"]
    influx_token = config["influx"]["token"]

    measurement_points = []

    if inverter_enabled:
        measurement_points.append(getInverterValues(config))

    if vzlogger_enabled:
        measurement_points.append(getVzloggerValues(config))

    client = influxdb_client.InfluxDBClient(
        url=influx_url,
        token=influx_token,
        org=influx_org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    try:
        write_api.write(bucket=influx_bucket, org=influx_org, record=measurement_points)
    except:
        if debug_output == "true":
            print("Write to InfluxDB failed. Is server offline?")

main()