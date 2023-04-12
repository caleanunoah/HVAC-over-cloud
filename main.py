import datetime
import json
import time
import boto3
import BoC
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


if __name__ == '__main__':
    sensorID = '12345678-91011-4447-bd53-17f3781c97a'

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

    time.sleep(2)
    print(BN.sensors)
    ppm = BN.readAll(ip="192.168.1.254", n=[513])['Analog_input 513']

    # Write to DB
    qry = "UPDATE sensors SET PPM = '" + ppm + "', PPMDateTime = '" + str(datetime.datetime.now()) + "' WHERE SensorID = '" + sensorID + "';"

    db.query(qry)
    db.query(db.queries['COMMIT'])

    print(db.query(db.queries['SENSOR SELECT']))

    # Exit function to close DB connection and cursor
    db.terminate()











