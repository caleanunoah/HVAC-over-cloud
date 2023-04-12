import uuid
import BAC0
import time
import datetime
import json
import math
from boto3.dynamodb.conditions import Key
import matplotlib.pyplot as plt


MAX_FILE_SIZE = 4*1024*1024         # File size maximum (4 MB)
local_ipv4_addr = "192.168.128.48"  # IPv4 Address - local machine's Wireless LAN
yabe_virtual_port = "64875"         # YABE generates port for simulation (new # each time ROOM SIM is started)
BAC0_port = "47808"                 # This is a defined in BACnet as the port #
n = [0]                             #


def readPresentValueAnalogInput(bacnet,
                    n,
                    local_ip_addr,
                    port):
    """
    @param bacnet: BACnet connection
    @param n: list of Object IDs to read from.
    @param local_ip_addr: # local machine's wireless LAN ipv4 address
    @param yabe_virtual_port: # YABE generates port for simulation (new # for new simulation)
    @return: data read from the Object ID list on the BACnet network
    """
    data = {}
    for x in n:
        # Initialize BACnet device ID's
        obj_id = str(x)

        # Connect to the BACnet simulator using the IP address and port number
        value = bacnet.read(local_ip_addr + ":" + port + " analogInput " + obj_id + " presentValue")
        #value = str(value)
        data["Analog_input " + obj_id] = value

    return data


def readPresentValueAnalogValue(bacnet,
                    n,
                    local_ip_addr,
                    yabe_virtual_port):
    """
    @param bacnet: BACnet connection
    @param n: list of Object IDs to read from.
    @param local_ip_addr: # local machine's wireless LAN ipv4 address
    @param yabe_virtual_port: # YABE generates port for simulation (new # for new simulation)
    @return: data read from the Object ID list on the BACnet network
    """
    data = {}
    for x in n:
        # Initialize BACnet device ID's
        obj_id = str(x)

        # Connect to the BACnet simulator using the IP address and port number
        value = bacnet.read(local_ip_addr + ":" + yabe_virtual_port + " analogValue " + obj_id + " presentValue")
        value = str(value)
        data["Analog_value" + obj_id] = value

    return data

def readPresentValueBinaryInput(bacnet,
                    n,
                    local_ip_addr,
                    port):
    """
    @param bacnet: BACnet connection
    @param n: list of Object IDs to read from.
    @param local_ip_addr: # local machine's wireless LAN ipv4 address
    @param yabe_virtual_port: # YABE generates port for simulation (new # for new simulation)
    @return: Present value read from the device ID list on the BACnet network
    """
    data = {}
    for x in n:
        # Initialize BACnet device ID's
        obj_id = str(x)

        # Connect to the BACnet simulator using the IP address and port number
        value = bacnet.read(local_ip_addr + ":" + port + " binaryInput " + obj_id + " presentValue")
        value = str(value)
        data["Binary_input " + obj_id] = value

    return data


def readPresentValueBinaryValue(bacnet,
                    n,
                    local_ip_addr,
                    yabe_virtual_port):
    """
    @param bacnet: BACnet connection
    @param n: list of Object IDs to read from.
    @param local_ip_addr: # local machine's wireless LAN ipv4 address
    @param yabe_virtual_port: # YABE generates port for simulation (new # for new simulation)
    @return: data read from the device ID list on the BACnet network
    """
    data = {}
    for x in n:
        # Initialize BACnet device ID's
        obj_id = str(x)

        # Connect to the BACnet simulator using the IP address and port number
        value = bacnet.read(local_ip_addr + ":" + yabe_virtual_port + " binaryValue " + obj_id + " presentValue")
        value = str(value)
        data["Binary_input " + obj_id] = value

    return data


def iterate_dict(dict, count, nested=True):
    """
    :param dict:  dictionary of Floors. Each Floor has various rooms that contain an RLDS
    :param count: Boolean flag to see if we need to count RLDS in dict (True) or just print results (False)
    :param nested: Boolean flag to indicate a dict that has dictionaries as values. True
    :return count: Number of RLDS
    """
    keys = dict.keys()
    counter = 0  # Count how many RLDS

    for key in keys:
        print()
        print("Floor: " + str(key))           # Floor Number
        #print("Rooms with RLDS:   " + str(dict[key]))     # Dict of Rooms + RLDS'

        # If nested is True then go through each sub-dictionary
        if nested:
            subkeys = dict[key].keys()
            for subkey in subkeys:
                print("     Room Name:           " + str(subkey))                # Room Name
                print("     RLDS #:              " + str(dict[key][subkey]))     # RLDS Number
                counter = counter + 1
                print()
    if count:
        return counter
    else:
        return None

def get_building_ids(table):
    #all_items = table.scan()['Items']
    item_ids = [site["building_ID"] for site in table.scan()['Items']]
    #return all_items, item_ids
    return item_ids

def float_to_int(ppm):
    int_ppm = math.floor(ppm)
    if int_ppm < 0:
        raise ValueError("Error - ppm is less than 0 which is outside valid range. \n")
    elif int_ppm > 1000:
        raise ValueError("Error - ppm exceeds 1000 which is outside of valid range. \n")

    return int_ppm

def db_write(table, ppm, alarm, ppm_dict):

    with table.batch_writer() as batch:
        for _id in ppm_dict:
            #print(_id)
            batch.put_item(Item={"building_ID": "254dc4fa-af74-4ee7-8cab-0c54d237479a",
                                    "rlds_ID": "5f011efc-3fd0-4e1e-b877-1499defbb64f",
                                    "ppm": ppm,
                                    "alarm_status": alarm,
                                    "datetime": str(datetime.datetime.now())
                                    })

def display_bacnet_connection(bacnet):
    bacnet.whois()
    print("\nBACNET Devices: ")
    print(bacnet.devices)               # All devices on the network
    #myController = bacnet.devices[0]
    #print("\nController ")
    #print(myController[0])              # 301C Controller

def initialize_bacnet(ip, port):
    try:
        pass
    except:
        pass
    return BAC0.lite(ip=ip, port=port)

def graph_ppm(samples, graph_y):
    plt.plot(graph_y)
    plt.ylabel("PPM")
    plt.xlabel("Sample, N")
    plt.title("PPM Measured for " + str(samples) + " samples")
    plt.show()

#########################
#  Class definitions
#########################

class RLDS:

    def __init__(self, room):
        self.room = room
        self._id = str(uuid.uuid4())
        self.PPM = "Not Initialized"

    def initializeBACnet(self, local_ipv4_addr, bacnet_read_port, bacnet_intialize_port):
        self.local_ipv4_addr = local_ipv4_addr
        self.bacnet_read_port = bacnet_read_port
        self.data = {}
        self.bacnet = BAC0.lite(ip=self.local_ipv4_addr, port=bacnet_intialize_port)
        return self.bacnet

    def readPPM(self, ip, n):
            """
            @param bacnet: BACnet connection
            @param n: list of Object IDs to read from.
            @param local_ip_addr: # local machine's wireless LAN ipv4 address
            @param yabe_virtual_port: # YABE generates port for simulation (new # for new simulation)
            @return: data read from the device ID list on the BACnet network
            """
            for x in n:
                # Initialize BACnet device ID's
                obj_id = str(x)

                # Connect to the BACnet simulator using the IP address and port number
                value = self.bacnet.read(ip + ":" + self.bacnet_read_port + " analogInput " + obj_id + " presentValue")
                self.PPM = value
                value = str(value)
                self.data["Analog_input " + obj_id] = value

            return self.data

    def writePPM(self, bacnet, table):
        print(bacnet.ip)

    def write_to_file(self, file_name):
        file1 = open(file_name, "a")
        file1.write(json.dumps(self.data,  indent=2))
        file1.close()

class Site:

    def __init__(self, name):
        self._id = str(uuid.uuid4())
        self.name = str(name)
        self.rlds = {}

    def add_rlds(self, desired_site, existing_sites, floor, room):

        for i in range(0, len(existing_sites)):
            if desired_site == list(existing_sites)[i]['building_ID']:
                if self.rlds:
                    for i in range(0, len(self.rlds)):
                        try:
                            self.rlds[str(desired_site)][floor].append(RLDS(room))
                        except KeyError:
                            self.rlds[str(desired_site)][floor] = [RLDS(room)]
                else:
                    print("rlds empty. Adding entry")
                    self.rlds[str(desired_site)] = {floor: [RLDS(room)]}
                    break
            else:
                pass

        return self.rlds




if __name__ == "__main__":

    # Create site and add multiple RLDS'
    NEU2 = Site("NEU")
    VGH = Site("VGH")

    existing_sites = [
        {'building_ID': 'b28220b5-26be-48cf-8f0b-3be807dba0ae', 'site_name': 'Neighbourhood Neighbourhood Utility'},
        {'building_ID': 'd6eea20b-1c59-4859-8188-442fa6632c40', 'site_name': 'Vancouver General Hospital'}]

    desired = "b28220b5-26be-48cf-8f0b-3be807dba0ae"


    NEU2.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=1, room=101)
    NEU2.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=2, room=202)
    NEU2.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=4, room=202)
    NEU2.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=7, room=202)
    NEU2.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=7, room=3202)


    desired = "d6eea20b-1c59-4859-8188-442fa6632c40"

    VGH.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=1, room=1000)
    VGH.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=2, room=1010)
    VGH.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=3, room=2020)
    VGH.add_rlds(desired_site=desired, existing_sites=existing_sites, floor=3, room=3000)

    time.sleep(1)
    print(NEU2.rlds)
    print(VGH.rlds)
    print(" __________________________ ")

    # Write to local .txt file
    '''
    fp = "PPM_Data"
    
    while True:

        NEU.rlds[1][0].rlds.readPPM(n=n)
        file_path = 'C:/Users/Operator/PycharmProjects/pythonProject/BoC/' + fp
        try:
            file_size = os.path.getsize(file_path)
            print("File Size is :", file_size, "bytes")

            # TODO: Take File size and if too big, write to a different file!!!
            if file_size > MAX_FILE_SIZE:
                fp = "PPM2"
            else:
                fp = "PPM_Data"

        except FileNotFoundError as err:
            print("No file found... Creating file called: " + fp)


        NEU.rlds[1][0].rlds.write_to_file(fp)
        time.sleep(10)
    '''





