import datetime
import json
import time
import uuid

import boto3
import BoC
import BAC0
from lib.DB import DB
from lib.Sensor import BacnetSensor, AnalogVoltageSensor, AnalogCurrentSensor
from lib.SensorNetwork import BacnetSensorNetwork, AnalogVoltageSensorNetwork, AnalogCurrentSensorNetwork

# Define some constants
# TODO: Move this outside of code and store each buildings IP/Honeywell device IP info separately
local_ipv4_addr = "192.168.1.70/24"                      # IPv4 Address - local machine's Wireless LAN
honeywell_301C_ipv4_addr = "192.168.1.254"               # IPv4 Address - Honeywell 301C Controller - IPv4 address
ethernet_ipv4_addr = "192.168.1.80/24"                   # IPv4 Address - Ethernet switch (type = managed)
yabe_room_sim_port = "55481"                             # YABE generates port for simulation (new # each time ROOM SIM is started)
BAC0_port = "47808"                                      # This is a defined in BACnet as the port #
BAC0_port_sim = "47809"
MAX_SAMPLE_PERIOD = 720                                  # Max sample period (seconds)
OBJ_ID_PPM = [513]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_BUZZ = [46360]                                       # BACnet ID of PPM reading found using (YABE: https://sourceforge.net/projects/yetanotherbacnetexplorer/)
OBJ_ID_SIM = [0]
data = {}
MAX_FILE_SIZE = 4*1024*1024                             # File size maximum (4 MB)

# Parameters that the user will provide implicitly or explicitly
# TODO Get params from user instead of hardcode
floor = 40
room = 50
mode = 'w'
SAMPLE_PERIOD_S = 1                                        # Sample period (seconds)
samples = 10

def get_data(bacnet):
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'rlds_ID': "rid_123",
        'sensor_ID': 'sid_1',
        'ppm': bacnet.read("192.168.1.72/24" + ":" + "47808" + " analogInput " + "513" + " presentValue"),
        'alarm_status': 'inactive'
    }

def generate(stream_name, kinesis_client, bacnet):
    while True:
        data = get_data(bacnet)
        print(data)
        time.sleep(60)
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey='partitionkey')

if __name__ == '__main__':
    bacnet = BAC0.lite(ip="192.168.1.75/24", port="47808")
    bacnet.whois()  # Prints 301C's IPv4 192.168.1.72
    STREAM_NAME = "OrangePi"

    print(bacnet.devices)

    #value = bacnet.read("192.168.1.72/24" + ":" + "47808" + " analogInput " + "513" + " presentValue")
    #print(value)
    k_client = boto3.client('kinesis', region_name='us-west-2')
    print("Client Resource to Kinesis successfully created")
    generate(stream_name=STREAM_NAME, kinesis_client=k_client, bacnet=bacnet)









