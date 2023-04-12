import datetime
import json
import time
import boto3
import BoC
from lib.DB import DB
from lib.Sensor import BacnetSensor, AnalogVoltageSensor, AnalogCurrentSensor
from lib.SensorNetwork import BacnetSensorNetwork, AnalogVoltageSensorNetwork, AnalogCurrentSensorNetwork
from lib.SiteKeyMapping import SiteKeyMapping as mapping

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

    #TODO: PLACE INSIDE CONFIG FILE AND LOAD PARAMS
    currentSite = "NEU"     # Site data the user is requesting
    currentSiteID = '7327de65-0f0e-4e99-94f7-8f74f5f3962f'

    # Get site + sensor configuration from DB
    db = DB()
    db.connect()
    db.query(db.queries['USE'])

    # Find the site ID
    qry = 'SELECT * FROM site WHERE SiteID= "' + currentSiteID + '";'
    userSiteID = db.query(qry)[0][0]

    # Find the building ID
    qry = 'SELECT * FROM buildings WHERE SiteID= "' + currentSiteID + '";'
    userBuildingID = db.query(qry)[0][0]

    # Find the RLDS IDs
    # TODO: use iterator to find the RLDS ID
    qry = 'SELECT * FROM RLDS WHERE BuildingID= "' + userBuildingID + '";'
    userRLDSID1 = db.query(qry)[0][0]
    userRLDSID2 = db.query(qry)[1][0]

    # Find the sensor data
    qry = 'SELECT * FROM sensors WHERE LeakSystemID= "' + userRLDSID1 + '";'
    allSensors = db.query(qry)
    print(allSensors)
    sensorsID = []
    print("\n Reading for sensors in ")
    for sensor in allSensors:
        sensorsID.append(sensor[0])
        print("\tSensor ID: " + str(sensor[0]) + " has PPM: " + str(sensor[1]) + " (at " + str(sensor[2]) + ")")


    # Initialize Sensor Network (BACNET)
    BN = BacnetSensorNetwork()
    SN1 = BacnetSensor(local_ipv4_addr="192.168.1.80", bacnet_read_port="47808", bacnet_intialize_port="47808")
    BN.addSensors(SN1)

    time.sleep(1)
    ppm = SN1.read(ip="192.168.1.254", n=[513])['Analog_input 513']
    sensorID = '12345678-91011-4447-bd53-17f3781c97a'

    datetime = datetime.datetime.now()

    # Write to DB
    qry = "UPDATE sensors SET PPM = '" + ppm + "', PPMDateTime = '" + str(datetime) + "' WHERE SensorID = '" + sensorID + "';"
    print(qry)
    db.query(qry)

    print(db.query(db.queries['SENSOR SELECT']))
    # Close the DB objects
    db.cursor.close()
    db.close()











