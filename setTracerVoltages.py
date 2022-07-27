#!/usr/bin/python
import sys
import datetime
import time
import minimalmodbus
from influxdb import InfluxDBClient
from SolarTracer import *

voltageRegStart = OverVoltageDisconnect
voltageNames = ["OverVoltageDisconnect","ChargingLimitVoltage","OverVoltageReconnect","EqualizationVoltage","BoostVoltage","FloatVoltage",
            "BoostReconnectVoltage","LowVoltageReconnect","UnderVoltageRecover","UnderVoltageWarning",
            "LowVoltageDisconnect", "DischargingLimitVoltage"]

lifepo  = [31.20,29.20,29.00,29.00,29.00,27.60,26.40,24.80,25.00,24.00,22.00,21.60]
flooded = [32.00,30.00,30.00,29.60,29.60,27.60,26.40,25.20,24.40,24.40,22.20,21.20]

up = SolarTracer()
if (up.connect() < 0):
	print("Could not connect to the device")
	exit -2

# get timestamps
localtime = time.localtime()
timestamp = time.strftime("%H:%M:%S", localtime)
timestamp = datetime.datetime.utcnow()

# form a data record
print("UTC timestamp:", timestamp)
print("BatteryType (0=USER):", up.readParam(BatteryType,0))
print("BatteryCapacity, Ah :", up.readParam(BatteryCapacity,0))
print()

idx = 0
for param in voltageNames:
    currentVolt = up.readParam(voltageRegStart + idx)

    # This will set voltages to LiFePO4, 8s, 24V battery
    newVolt = lifepo[idx]

    print('{:<23}'.format(param), ":", currentVolt, end=' ')
    
    if (newVolt != currentVolt):
        print("->", newVolt, "...", end=' ')
        if (up.writeParam(voltageRegStart+idx, newVolt) < 0): print("FAILED!")
        else: print("OK")
        break
    else: print()
    idx = idx + 1
