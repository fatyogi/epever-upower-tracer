#!/usr/bin/python
import sys
import time
from UPower import *


up = UPower()
if (up.connect() < 0):
	print("Could not connect to the device")
	exit -2

print(up.getBatteryType())
#if (up.setBatteryType("User") < 0):
#	print "Error setting battery"
#	exit -1

#print "New battery type:", up.getBatteryType()
#print "Battery Capacity", up.getBatteryCapacity()
#print "Battery Capacity", up.getBatteryCapacity()
print("Charge priority:", up.getChargePriority())
print("Setting charge priority", up.setChargePriority("Solar Priority"))
print("New Charge priority:", up.getChargePriority())

#print "Inverter status", up.getInverter()
#print "IV status", up.getIV()
#print "AC status", up.getAC()
#print "Switching AC off", up.switchAC(OFF)
#time.sleep(5)
#print "AC status", up.getAC()

#stat = up.instrument.read_register(STchrg, 0, 4)
#print "Status charge:", bin(stat)

up.reset()
print("Current voltage", up.readReg(0x351D))
#BAamps = 0x351E
#BAwattL = 0x351F
#BAvoltage = 0x354C
#BAtemp = 0x354F
#BAperc = 0x3550


