#!/usr/bin/python3

import sys
import datetime
import time
import minimalmodbus
from SolarTracer import *

up = SolarTracer()
if (up.connect() < 0):
	print ("Could not connect to the device")
	exit -2

# get timestamps
timestamp = datetime.datetime.utcnow()

FloatNo = 0.0

PVvolt = up.readReg(PVvolt) + FloatNo
PVamps = up.readReg(PVamps) + FloatNo
PVwatt = round(PVvolt * PVamps, 2)
PVkwhTotal = up.readReg(PVkwhTotal);
PVkwhToday = up.readReg(PVkwhToday);

BAvolt = up.readReg(BAvolt)
BAamps = up.readReg(BAamps) + FloatNo
BAperc = up.readReg(BAperc) * 100
BAtemp = up.readReg(BAtemp)

ControllerTemp = up.readReg(ControllerTemp)

DCvolt = up.readReg(DCvolt) + FloatNo
DCamps = round(up.readReg(DCamps), 2) + FloatNo
DCwatt = round(DCvolt * DCamps, 2) + FloatNo
DCkwhTotal = up.readReg(DCkwhTotal)
DCkwhToday = up.readReg(DCkwhToday)

## form a data record
#body_solar = [
#    {
#        "t": timestamp,
#        "d": {
#            # Solar panel
#            "PVV": PVvolt,
#            "PVI": PVamps,
#            "PVW": PVwatt,
#            "PVKWh": PVkwhTotal,
#            "PVKWh24": PVkwhToday,
#            # Battery
#            "BV": BAvolt,
#            "BI": BAamps,
#            "BSOC": BAperc,
#            "BTEMP": BAtemp,
#            "CTEMP": ControllerTemp,
#            # Load
#            "LV": DCvolt,
#            "LI": DCamps,
#            "LW": DCwatt,
#            "LKWh": DCkwhTotal,
#            "LKWh24": DCkwhToday
#        }
#    }
#]
#print (body_solar)

# print csv format
print('%.3f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' %
        (timestamp.timestamp(),
        PVvolt, PVamps, PVwatt, PVkwhTotal, PVkwhToday,
        DCvolt, DCamps, DCwatt, DCkwhTotal, DCkwhToday,
        BAvolt, BAamps, BAperc, BAtemp, ControllerTemp))



