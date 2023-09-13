try:
    import sys
    import datetime
    import pytz
    import json
    import time
    import uuid
    import BAC0.core.io.IOExceptions as BACError
    import random
    import numpy as np
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
except ImportError as err:
    print("IMPORT ERROR in one of the 3rd party libraries")

try: # Custom libraries
    import BAC0
    import lib
    #import BoC
except ImportError as err:
    print("IMPORT ERROR in one of the custom libraries")

def get_data(bacnet_cnx, device_ID):
    dt = datetime.datetime.now(pytz.timezone('Canada/Pacific')).isoformat()
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'rlds_ID': "NEU",
        'sensor_ID': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + device_ID + " objectIdentifier"),
        'sensor_name': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + device_ID + " objectName"),
        'ppm': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + device_ID + " presentValue"),
        'ppm_status_flags': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + device_ID + " reliability"),
        'out_of_service': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + device_ID + " outOfService"),

    }

def get_spoof_data(bacnet_cnx, device_ID):
    dt = datetime.datetime.now(pytz.timezone('Canada/Pacific')).isoformat()
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'rlds_ID': "NEU",
        'sensor_ID': "f77a9fc0-c3ea-465a-ac6d-5afbdc91e516",
        'sensor_name': "Sensor1",
        'ppm': random.randint(0, 1023),
        'ppm_status_flags': "inactive",
        'out_of_service': "false",

    }

'''
def generate(stream_name, kinesis_client, bacnet_cnx):
    while True:
        for id in lib.OBJ_ID_PPM:
            data = get_data(bacnet_cnx, id)
            print(data)

            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(data),
                PartitionKey='partitionkey')

        time.sleep(60)
'''


if __name__ == '__main__':
    print("Starting main.py")

    try:
        print("Creating BACnet connection")
        bacnet = BAC0.lite(ip=lib.ipv4_address, port=lib.BAC0_port)
        bacnet.whois()  # Prints 301C's IPv4 192.168.1.72
        #print(bacnet.devices)
        #time.sleep(1)
        controller = BAC0.device(address=lib.honeywell_301C_ipv4_addr, device_id=1, network=bacnet)
        #print(controller.points)
    except AttributeError as err:
        print(err)
        print("\nBACNET Attribute Error. Could not initialize BACnet, check variable names are correctly spelled/declared")
    except BACError.InitializationError as err:
        print(err)
        print("\nBACNET Initialization Error. Check the IP addresses and ports are correct in the ~/lib folder")

    try:
        for id in lib.OBJ_ID_PPM:
            data = get_spoof_data(bacnet, id)
            print(data)
    except BACError.NoResponseFromController as err:
        print(err)
        print("\nNo Response from controller. It is likely the controller that has disconnected. Double check wired connections and IP addressess")
    except NameError as err:
        print(err)
        print("\nName Error. It is likely the BACnet connection did not initialize so when we tried to get data there is nothing called 'bacnet'. Double check the initialization of the BACnet cnx")

    try:
        bucket = "test-bucket"
        client = InfluxDBClient(url="http://localhost:8086",
                                token="K5AKcnKQuQEIZ6dMXwxH2kzd95DNftQLWa6516fJhEAQkD6V_wlcjdd596AywTbniwyMdV2hDUajoV2b6RevDA=="
                                , org="Operator Technologies")
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = Point("my_measurement").tag("site", data['rlds_ID']).field("ppm", data['ppm'])
        write_api.write(bucket=bucket, record=p)

    except TypeError as err:
        pass

    '''
    # ONLINE

    generate(stream_name="OrangePi",
             kinesis_client=boto3.client('kinesis', region_name='us-west-2'),
             bacnet_cnx=bacnet)
    '''

    '''
    # OFFLINE
    while True:
        local_data = json.dumps(get_data(bacnet), indent=2)
        print(local_data)
        
        f = open("local_database.txt", "a")
        f.write(local_data)
        f.close()
        # open and read the file after the appending:
        f = open("local_database.txt", "r")
        print(f.read())
        f.close()

        time.sleep(60)
    '''






