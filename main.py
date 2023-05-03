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

from lib.DB import DB
from lib.Sensor import BacnetSensor, AnalogVoltageSensor, AnalogCurrentSensor
from lib.SensorNetwork import BacnetSensorNetwork, AnalogVoltageSensorNetwork, AnalogCurrentSensorNetwork


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

def get_data(bacnet):
    dt = datetime.datetime.now(pytz.timezone('Canada/Pacific')).isoformat()
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'rlds_ID': "rid_123",
        'sensor_ID': 'sid_1',
        'ppm': bacnet.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + lib.OBJ_ID_PPM[0] + " presentValue"),
        'ppm_status_flags': bacnet.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + lib.OBJ_ID_PPM[0] + " statusFlags"),
        'ppm_reliability': bacnet.read(lib.honeywell_301C_ipv4_addr + ":" + lib.BAC0_port + " analogInput " + lib.OBJ_ID_PPM[0] + " reliability"),
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


    bacnet = BAC0.lite(ip=lib.ipv4_pc, port="47808")
    bacnet.whois()  # Prints 301C's IPv4 192.168.1.72
    print(bacnet.devices)

    #ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=3000)
    #plt.show()

    print("Client Resource to Kinesis successfully created")

    time.sleep(1)
    generate(stream_name="OrangePi",
             kinesis_client=boto3.client('kinesis', region_name='us-west-2'),
             bacnet=bacnet)











