#!/usr/bin/python
import sys
import datetime
import time
import minimalmodbus
from influxdb import InfluxDBClient
from SolarTracer import *


up = SolarTracer()
if (up.connect() < 0):
	print "Could not connect to the device"
	exit -2

# get timestamps
localtime = time.localtime()
localstamp = time.strftime("%H:%M:%S", localtime)
timestamp = datetime.datetime.utcnow()

# form a data record
print "Local time:", localstamp
print "UTC timestamp:", timestamp
print


up.setBatterySettings(batteryLiFePO4, 300, 12)
print
up.printBatterySettings()
