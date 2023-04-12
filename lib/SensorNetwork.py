import BAC0
import uuid
import json
from .Sensor import BacnetSensor, AnalogCurrentSensor, AnalogVoltageSensor

class InformalSensorNetworkInterface:
    def __init__(self):
        self.sensors = {}

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
        self.sensors = []

    def displaySensors(self):
        print("\nDisplaying all sensors in network: ")
        for sensor in self.sensors:
            print("\t" + sensor)

    def addSensors(self, sensor):
        self.sensors.append(sensor)

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

    def addSensors(self):
        id = str(uuid.uuid4())
        self.sensors[id] = AnalogVoltageSensor()
        print("Added voltage sensor with ID: " + id)

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

    def addSensors(self):
        id = str(uuid.uuid4())
        self.sensors[id] = AnalogCurrentSensor()
        print("Added current sensor with ID: " + id)

    def removeSensors(self):
        pass


if __name__ == "__main__":
    bacnet_network = BacnetSensorNetwork()
    bacnet_network.initializeNetwork("192.168.1.80", "47808", "47808")
    print(bacnet_network.protocol)
    print(bacnet_network.sensors)

    bacnet_network.addSensors()
    bacnet_network.addSensors()
    bacnet_network.addSensors()

    bacnet_network.displaySensors()


    #print(bac.read("192.168.1.254", [513]))