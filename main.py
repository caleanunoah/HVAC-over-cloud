import datetime
import pytz
import json
import time
import uuid

import boto3
import sys
import BAC0
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
plt.rcParams.update({'font.size': 25})

import lib
#import BoC

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []


def animate(i, xs, ys):
    """
    Credit to Author SHAWN HYMEL [https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time]
    """
    data = get_data(bacnet)
    print(data['ppm'])

    ys.append(float(data['ppm']))
    xs.append(datetime.datetime.now().strftime('%H:%M:%S'))

    xs = xs[-20:]
    ys = ys[-20:]

    ax1.clear()
    ax1.plot(xs, ys)

    plt.xlabel('Event Time')
    plt.ylabel('PPM')
    plt.title('Live graph of PPM')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


def get_data(bacnet_cnx):
    dt = datetime.datetime.now(pytz.timezone('Canada/Pacific')).isoformat()
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'rlds_ID': "rid_123",
        'sensor_ID': 'sid_1',
        'ppm': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + lib.OBJ_ID_PPM[0] + " presentValue"),
        'ppm_status_flags': bacnet_cnx.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + lib.OBJ_ID_PPM[0] + " statusFlags")
    }

def generate(stream_name, kinesis_client, bacnet_cnx):
    while True:
        data = get_data(bacnet_cnx)
        print(data)

        time.sleep(60)

        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey='partitionkey')


if __name__ == '__main__':

    bacnet = BAC0.lite(ip=lib.ipv4_orangepi, port="47808")
    bacnet.whois()  # Prints 301C's IPv4 192.168.1.72
    print(bacnet.devices)

    #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=3000)
    #plt.show()

    # ONLINE
    '''
    generate(stream_name="OrangePi",
             kinesis_client=boto3.client('kinesis', region_name='us-west-2'),
             bacnet_cnx=bacnet)
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







