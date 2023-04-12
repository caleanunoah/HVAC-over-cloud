import unittest
import boto3
import BAC0.core.io.IOExceptions as BAC0Error
import BoC

my_ipv4 = "192.168.128.48"
BACNET_PORT = 47808
yabe_room_sim_port = "64841"
n = [0, 1, 2]

class MyTestCase(unittest.TestCase):
    def test_bacnet(self):
        bacnet = BoC.initBACNET(my_ipv4, BACNET_PORT)
        self.assertIsNotNone(bacnet, msg="Test 1 Step 1 Failed. Double check WLAN IPv4 matches ipconfig")

        try:
            data = BoC.readPresentValueAnalogInput(bacnet, n, my_ipv4, yabe_room_sim_port)
            for item in data:
                self.assertTrue(int(data[str(item)]) >= 0)
                self.assertTrue(int(data[str(item)]) <= 1000)

        except BAC0Error.NoResponseFromController as err:
            print("\n" + str(err))

    def test_db(self):
        # Setup low-level client + resources for DynamoDB
        client = boto3.client('dynamodb', region_name='us-east-1')
        self.assertIsNotNone(client, msg="Test 2; Step 1 Failed. Client is None")

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.assertIsNotNone(dynamodb, msg="Test 2; Step 2 Failed. DynamoDB is None")
        # Create table called "PPM"
        table = dynamodb.Table('PPM')
        self.assertIsNotNone(table, msg="Test 2 Step 3 Failed. Table is None")


if __name__ == '__main__':
    unittest.main()
