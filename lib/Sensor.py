from abc import abstractmethod
import BAC0


class InformalSensorInterface:
    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def add(self, a, b):
        return a+b

class BacnetSensor(InformalSensorInterface):
    def __init__(self):
        super().__init__()

    def read(self, ip, n):
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

    def test(self, a, b):
        return a+b

class AnalogVoltageSensor(InformalSensorInterface):
    def __init__(self):
        super().__init__()

    def read(self):
        pass

    def test(self, a, b):
        return a*b

class AnalogCurrentSensor(InformalSensorInterface):
    def __init__(self):
        super().__init__()

    def read(self):
        pass


if __name__ == "__main__":
    pass
