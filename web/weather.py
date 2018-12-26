#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
import Adafruit_DHT
import glob
import time
from datetime import datetime

import os
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web.settings"
)
from django.conf import settings
django.setup()
from weatherstation.models import *

# The break of 2 seconds will be configured here
sleeptime = 600

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHTSensor = Adafruit_DHT.DHT11 # this is same as 11
 
# The pin which are connected with the sensors will be declared here
GPIO_hum_pin = 4
GPIO_temp_pin = 17
 
# the one-wire input pin for the KY-001 sensor will be declared and the integrated pullup-resistor will be enabled
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_temp_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# After the enabling of the pullup-resistor you have to wait till the communication with the DS18B20 (KY-001) sensor has started
print ('Initializing the communication with DS188B20 temperature sensor. ')
base_dir = '/sys/bus/w1/devices/'
while True:
    try:
        device_folder = glob.glob(base_dir + '28*')[0]
        break
    except IndexError:
        time.sleep(0.5)
        continue
device_file = device_folder + '/w1_slave'
 
# The function to read currently measurement at the sensor will be defined.
def TemperaturMessung():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Analysis of temperature: At the Raspberry Pi
# noticed one-wire slaves at the directory /sys/bus/w1/devices/
# will be assigned to a own subfolder.
# In this folder is the file in which the data from the one-wire bus will be saved.<br /># In this function, the data will be analyzed, the temperature read and returned to the main program.<br />
def TemperaturAuswertung():
    lines = TemperaturMessung()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = TemperaturMessung()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
# To initialise, the sensor will be read "blind"
TemperaturMessung()
print('Initialization ready. ') 

print('Starting the measurements. ')
 
try:
    while(1):
        # Measurement will be started and the result will be written into the variables
        humid, temper = Adafruit_DHT.read_retry(DHTSensor, GPIO_hum_pin)
        ky001_temp = TemperaturAuswertung()
        
        if humid is not None and temper is not None and ky001_temp is not None:
            # The result will be shown at the console
            print(datetime.now().strftime('%d.%m.%Y klo %H:%M')) 
            print('DHT11 temp. = {:.0f} °C   |  KY-001 temp. = {:.1f} °C  | RH = {:.0f} %'.format(temper, ky001_temp, humid))
            print('')
            
            measurement = Measurement(date=datetime.now(), temperature=ky001_temp, humidity=humid)
            measurement.save()
            
            # Logging the measurements to .csv file 
            # with open("measurements_log.csv", "a") as log_file:
                # log_file.write('\n' + datetime.now().strftime('%d.%m.%Y;%H:%M') + ';{:.1f};{:.0f}'.format(ky001_temp, humid))

        
        # Because of the linux OS, the Raspberry Pi has problems with realtime measurements.
        # It is possible that, because of timing problems, the communication fails.
        # In that case, an error message will be displayed - the result should be shown at the next try.
        else:
            print('Error while reading - please wait for the next try!')

        time.sleep(sleeptime)
 
# Scavenging work after the end of the program
except KeyboardInterrupt:
    GPIO.cleanup()#!/usr/bin/python

