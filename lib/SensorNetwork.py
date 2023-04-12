import BAC0
import uuid
import time
import json
from lib.Sensor import BacnetSensor, AnalogCurrentSensor, AnalogVoltageSensor

class InformalSensorNetworkInterface:
    def __init__(self):
        self.sensors = []
        self.data = {}

    def initializeNetwork(self):
        pass

    def displaySensors(self):
        pass

    def addSensors(self):
        pass

    def removeSensors(self):
        pass


class BacnetSensorNetwork(InformalSensorNetworkInterface):
    def __init__(self):
        super().__init__()
        self.protocol = "BACN"

    def displaySensors(self):
        print("\nDisplaying all sensors in network: ")
        for sensor in self.sensors:
            print("\t" + sensor)

    def addSensors(self, sensor):
        self.sensors.append(sensor)

    def readAll(self, ip, n):
        for sensor in self.sensors:
            self.data = sensor.read(ip, n)
        return self.data


    def removeSensors(self, id):
        pass


class AnalogVoltageSensorNetwork(InformalSensorNetworkInterface):
    def __init__(self):
        super().__init__()
        self.protocol = "VOLT"

    def initializeNetwork(self):
        pass

    def displaySensors(self):
        pass

    def addSensors(self, sensor):
        self.sensors.append(sensor)

    def removeSensors(self):
        pass


class AnalogCurrentSensorNetwork(InformalSensorNetworkInterface):
    def __init__(self):
        super().__init__()
        self.protocol = "CURR"

    def initializeNetwork(self):
        pass

    def displaySensors(self):
        pass

    def addSensors(self, sensor):
        self.sensors.append(sensor)

    def removeSensors(self):
        pass


if __name__ == "__main__":
    local_ipv4_addr = "192.168.1.80"
    bacnet_read_port = "47808"
    bacnet_intialize_port = "47808"

    BN = BacnetSensorNetwork()
    SN1 = BacnetSensor(local_ipv4_addr=local_ipv4_addr, bacnet_read_port=bacnet_read_port, bacnet_intialize_port=bacnet_intialize_port)

    BN.addSensors(SN1)

    BN.readAll(ip="192.168.1.254", n=[513])

    time.sleep(1)