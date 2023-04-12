import datetime
import json
import time
import boto3
import os
import BoC
import matplotlib
from lib.DB import DB

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

# Setup low-level client + resources for DynamoDB
client = boto3.client('dynamodb', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb_sites = boto3.resource('dynamodb', region_name='us-east-1')

# Create connection to DynamoDB Tables
table_ppm = dynamodb.Table('PPM')                                   # Create table called "PPM"
table_sites = dynamodb_sites.Table('SITES')                         # Create table called "PPM"

# Parameters that the user will provide implicitly or explicitly
# TODO Get params from user instead of hardcode
building_ID = "254dc4fa-af74-4ee7-8cab-0c54d237479a"    # NEU
rlds_id = "5f011efc-3fd0-4e1e-b877-1499defbb64f"        # Chiller Room
floor = 40
room = 50
mode = 'w'
SAMPLE_PERIOD_S = 1                                        # Sample period (seconds)
samples = 10

######################################
# THIS IS SIMULATION CODE~!!
# IGNORE when using 301C
def main_sim(bacnet, freq, mode):
    for i in range(0, freq):
        print("\n\n____ Reading BACnet Data every " + str(SAMPLE_PERIOD_S) + " seconds ____")
        time.sleep(SAMPLE_PERIOD_S)

        for _id in OBJ_ID_SIM:
            # SIMULATION - READ ANALOG VALUE. Read data from BACnet Room simulation
            value = bacnet.read(local_ipv4_addr + ":" + yabe_room_sim_port + " analogInput " + str(_id) + " presentValue")  # Get PPM
            data[str(_id)] = value
            # Write after each read
            if mode == 'w':
                BoC.db_write(table_sites, data)


        print("Simulation Data is: " + json.dumps(data, indent=2))
        resp = table_sites.scan()
        data2 = resp['Items']
        print("Scanned DB Data is: " + json.dumps(data2, indent=2))

        # BATCH WRITE AFTER ALL READS
        ''' 
        # If user indicates DB write needed then save PPM in database
        #if mode == 'w':
        #    BoC.db_write(table_sites, data)
        # Query all items in the db to verify it wrote correctly
        #    resp = table_sites.scan()
        #    data2 = resp['Items']
        #    print("Scanned DB Data is: " + json.dumps(data2, indent=2))
        '''
######################################


######################################
def main(bacnet, mode, port, samples):
    # Find 301-C on BACnet network
    BoC.display_bacnet_connection(bacnet)
    ppm_list = []
    ppm_dict = {}

    for i in range(0, samples):
        # Now read 301C Objects over BACnet connection
        ppm_dict = BoC.readPresentValueAnalogInput(bacnet=bacnet,
                                                   n=OBJ_ID_PPM,
                                                   local_ip_addr=honeywell_301C_ipv4_addr,
                                                   port=port)
        time.sleep(2)
        alarm_dict = BoC.readPresentValueBinaryInput(bacnet=bacnet,
                                                        n=OBJ_ID_BUZZ,
                                                        local_ip_addr=honeywell_301C_ipv4_addr,
                                                        port=port)
        print("\nBACnet Data: Sample #" + str(i+1) + ": ")
        # print(ppm_dict)                                         # {"Analog_input 513":  "0.0"}

        ppm = ppm_dict['Analog_input ' + str(OBJ_ID_PPM[0])]                # "0.0"
        alarm_status = alarm_dict['Binary_input ' + str(OBJ_ID_BUZZ[0])]    # "inactive"
        ppm_int = BoC.float_to_int(ppm)

        print("Alarm status: ")
        print(alarm_status)                                         # {"Binary_input 46360": "0.0"}
        print(ppm_list)

        ppm_list.append(ppm_int)


        # If write enabled -> update PPM
        if mode == "w":
            BoC.db_write(table=table_sites,         # DynamoDB table name
                         ppm=ppm_int,                   # BoC ppm reading
                         alarm=alarm_status,
                         ppm_dict=ppm_dict)         # Other interesting BoC data
        time.sleep(SAMPLE_PERIOD_S)

    return ppm_list                                 # Return the PPM list to graph

######################################


if __name__ == '__main__':

    db = DB()
    db.connect()
    db.query("USE Operator_sites;")

    #res = db.query("INSERT INTO sensors VALUES ('12345678-91011-4447-bd53-17f3781c97a1', '0', '2023-04-11 2:34:57', 'ac780a17-b3b1-4442-b0e6-f6cdb00fb7fd');")
    #db.query("COMMIT;")
    #time.sleep(1)
    #print(res)

    found = db.query("SELECT * FROM sensors;")

    time.sleep(1)

    print(found)



    #sensor1 = db.query("SELECT * FROM sensors;")[0]
    '''
    sensor1_id = sensor1[0]
    sensor1_ppm = sensor1[1]
    sensor1_datetime = sensor1[2]
    sensor1_rlds = sensor1[3]

    print("\nSensor ID: " + str(sensor1_id))
    print("Sensor PPM: " + str(sensor1_ppm))
    print("Sensor Datetime: " + str(sensor1_datetime))
    print("Sensor's RLDS ID: " + str(sensor1_rlds))
    '''

    '''
    # Create BACet connection
    bacnet = BoC.initialize_bacnet(ip="192.168.1.80/24", port="47808")
    print("\nBACnet Initialized: ")
    print(bacnet)
    
    time.sleep(1)
    ppm_dict = BoC.readPresentValueAnalogInput(bacnet=bacnet,
                                               n=[513],
                                               local_ip_addr="192.168.1.254",
                                               port="47808")
    raw_ppm = int(ppm_dict['Analog_input 513'])
    print("\nPPM: ")
    print(raw_ppm)
    #VALUES = "('" + "12345678-9101-4447-bd53-17f3781c97a1" + "', '" + str(raw_ppm) + "', '" + "2023-04-11 2:34:57" + "', '" + sensor1_rlds + "');"
    res = db.query("INSERT INTO sensors VALUES ('12345678-91011-4447-bd53-17f3781c97a1', '0', '2023-04-11 2:34:57', 'ac780a17-b3b1-4442-b0e6-f6cdb00fb7fd');")[0]
    time.sleep(1)
    #print(res)
    '''
    #res = db.query("INSERT INTO sensors VALUES ('12345678-91011-4447-bd53-17f3781c97a1', '0', '2023-04-11 2:34:57', 'ac780a17-b3b1-4442-b0e6-f6cdb00fb7fd');")
    #print(res)

    db.cursor.close()
    db.close()











