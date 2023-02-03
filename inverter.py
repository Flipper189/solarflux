import requests
import json
import influxdb_client

def getInverterValues(config):
    measurement_points = []
    
    #get config
    debug_output = config["global"]["debug_output"]
    hostname = config["inverter"]["hostname"]
    measurement = config["inverter"]["measurement"]

    try:
        #get data from inverter
        url = requests.get("http://" + hostname + "/solar_api/v1/GetPowerFlowRealtimeData.fcgi", timeout=10)

        try:
            #parse data
            json_data = json.loads(url.text)
            inverter_list = json_data['Body']['Data']['Inverters']
            for inverter_number in inverter_list:
                inverter_data = json_data['Body']['Data']['Inverters'][inverter_number]
                total_kWh = inverter_data['E_Total'] / 1000
                point = influxdb_client.Point(measurement).tag("unit", "kWh").field("inverter_" + str(inverter_number), total_kWh)
                measurement_points.append(point)
                if debug_output == "true":
                    print("Total current: " + str(total_kWh) + " kWh")

        except:
            if debug_output == "true":
                print("failed to parse inverter data")

    except:
        if debug_output == "true":
            print("failed to get inverter data, is server offline?")

    return measurement_points
