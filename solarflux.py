import requests
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

config_file = open("config.json")
config_data = json.load(config_file)

global_debug_output = config_data["global"]["debug_output"]
inverter_hostname = config_data["inverter"]["hostname"]
influx_url = config_data["influx"]["url"]
influx_org = config_data["influx"]["org"]
influx_bucket = config_data["influx"]["bucket"]
influx_token = config_data["influx"]["token"]
influx_measurement = config_data["influx"]["measurement"]


def write_to_Console(total):
    print("Total current: " + str(total/1000) + " kWh")


def write_to_DB(inverter, total):
    try:
        client = influxdb_client.InfluxDBClient(
            url=influx_url,
            token=influx_token,
            org=influx_org
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = influxdb_client.Point(influx_measurement).tag("inverter", str(inverter)).tag("value", "total").field("kWh", total/1000)
        write_api.write(bucket=influx_bucket, org=influx_org, record=p)
    except:
        if global_debug_output == "true":
            print("failed to write to database")
        return

def read_Data(data_string):
    try:
        json_data = json.loads(data_string)
        inverter_list = json_data['Body']['Data']['Inverters']
        for inverter in inverter_list:
            inverter_data = json_data['Body']['Data']['Inverters'][inverter]
            total = inverter_data['E_Total']
            if global_debug_output == "true":
                write_to_Console(total)
            write_to_DB(inverter, total)
    except:
        if global_debug_output == "true":
            print("failed to parse data")
        return


def main():
    try: 
        url = requests.get("http://" + inverter_hostname + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
        data = url.text
        read_Data(data)
    except:
        if global_debug_output == "true":
            print("failed to get data from server")


main()
