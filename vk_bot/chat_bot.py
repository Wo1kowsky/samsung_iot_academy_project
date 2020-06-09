import vk_api
import ibmiotf.application
import time
import vk_bot.messaging as messaging
import pickle
import json

from credentials import token
from credentials import options
from vk_bot.src.database import Database

source_device_type = 'gas_sensor'
source_device_id = 'gas_sensor_1'
my_event = 'status'

# loading users' data
devices = {source_device_id: 'testtest'}
# users = {}
try:
    database = Database()
    database.connect()
    # dbfile = open('users.db', 'rb')
    # users = pickle.load(dbfile)
    # dbfile.close()
    # print(users)
except Exception as e:
    print(e)


# callback function for IBM cloud data listener
def my_callback(event):
    f = open('log.txt', 'a')
    f.write('{0} : {1}\n'.format(event.timestamp, event.data))
    f.close()
    print('{0} : {1}'.format(event.timestamp, event.data))
    print()

    code = devices[event.deviceId]
    users = database.db_get_users_with_device(code)
    # sending message to every subscribed user
    for user in users:
        # if event.data['Voltage'] in range(100, 200) and code in users[user]:
        if event.data['Voltage'] in range(100, 200):
            vk.method('messages.send', {'user_id': user[0], 'random_id': time.gmtime(),
                                        'message': 'Вам следует в ближайшее время проверить холодильник'})
        # elif event.data['Voltage'] in range(700, 800) and code in users[user]:
        elif event.data['Voltage'] in range(700, 800):
            vk.method('messages.send', {'user_id': user[0], 'random_id': time.gmtime(),
                                        'message': 'Вам следует СРОЧНО проверить холодильник!'})


# creating IBM cloud client object
client = ibmiotf.application.Client(options)
client.connect()
client.subscribeToDeviceEvents(deviceType=source_device_type, deviceId=source_device_id, event=my_event)
client.deviceEventCallback = my_callback

# creating vk_api client
vk = vk_api.VkApi(token=token)
messaging.messages_listening()
