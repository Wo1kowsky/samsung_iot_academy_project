import wiotp.sdk.device
import random
import time


def my_publish_callback():
    print(f'published: kek')


myConfig = {
    "identity": {
        "orgId": "9iwrg7",
        "typeId": "gas_sensor",
        "deviceId": "gas_sensor_1"
    },
    "auth": {
        "token": "hKaOVU(9r@ycaY2_+?"
    },
}

# Configure
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)

# Connect
client.connect()

for x in range(1000):
    # Send Data
    myData = {'Voltage': random.randint(1, 800)}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=my_publish_callback)
    time.sleep(10)

# Disconnect
client.disconnect()
