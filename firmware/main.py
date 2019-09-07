import time

start = time.time()

from machine import Pin, I2C
from time import sleep
import json

led = Pin(2, Pin.OUT)
led.value(True)

# importing authentification data
from auth import TOKEN
from auth import BROKER
from auth import CLIENT_ID
from auth import TOPIC
from auth import PWD
from auth import SSID


# deep sleep function
def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, msecs)
    machine.deepsleep()


import network

# creating wi-fi interface object
sta_if = network.WLAN(network.STA_IF)

# importing connection functions
from firmware.wi_fi import do_connect

from firmware import ads1x15

# creating ADC object using I2C interface
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
adc = ads1x15.ADS1115(i2c, 72, 5)
adc.gain = 1
# adc = machine.ADC(0)
red_led = Pin(12, Pin.OUT)
red_led.value(True)

# connecting to network
do_connect(sta_if, SSID, PWD)

# importing and creating mqtt object which connects to IBM cloud
import umqtt.simple as mqtt

client = mqtt.MQTTClient(CLIENT_ID, BROKER, user='use-token-auth', password=TOKEN)
client.connect()
sleep(1)

# reading data from ADC
payload = {'Voltage': adc.read(0)}

try:
    # publishing ADC data to IBM cloud
    client.publish(TOPIC, json.dumps(payload))
    print('Published: ', payload)
except OSError:
    print('Message was not published')

print('Im awake, but Im going to sleep')
sleep(5)
led.value(False)
end = time.time()
# deep sleep mode
deep_sleep(15000 - (end - start) * 1000)

# additional script which is used for sensor demonstration
"""
from machine import Pin, I2C
from time import sleep
import ads1x15
#import machine

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
adc = ads1x15.ADS1115(i2c, 72, 5)
adc.gain = 1
#adc = machine.ADC(0)
pin = Pin(14, Pin.OUT)
pin.value(False)
led = Pin(12, Pin.OUT)
led.value(True)
while True:
  print(adc.read(0))
  #print(adc.read())
  sleep(0.5)
"""
