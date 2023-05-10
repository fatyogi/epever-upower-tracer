#!/usr/bin/python3

import sys
import datetime
import time
import minimalmodbus
from influxdb import InfluxDBClient
from SolarTracer import *
import sdm_modbus

SDM_DEVICE="/dev/ttyXRUSB1"

# influx configuration - edit these
ifuser = "grafana"
ifpass = "solar"
ifdb   = "solar"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "solar"

up = SolarTracer()
if (up.connect() < 0):
	print ("Could not connect to the device")
	exit -2

# get timestamps
localtime = time.localtime()
timestamp = time.strftime("%H:%M:%S", localtime)
timestamp = datetime.datetime.utcnow()

# calculate compound values - did not work!
# sometimes it returns large NEGATIVE values
# temporarily coming back to the lower part of the word only
#PVwatt = up.readReg(PVwattH)
#PVwatt = ((int(PVwatt) << 16) + up.readReg(PVwattL));
#DCwatt = up.readReg(DCwattH)
#DCwatt = ((int(DCwatt) << 16) + up.readReg(DCwattL));

FloatNo = 0.0

PVvolt = up.readReg(PVvolt) + FloatNo
PVamps = up.readReg(PVamps) + FloatNo
PVwatt = round(PVvolt * PVamps, 2)

DCvolt = up.readReg(DCvolt) + FloatNo
DCamps = round(up.readReg(DCamps), 2) + FloatNo
DCwatt = round(DCvolt * DCamps, 2) + FloatNo

# dummy values - get the inverter and a metere (see SDM230 script)
(IVvolt,IVamps,IVwatt,IVison) = (0.0,0.0,0.0,1)

#print (f"\nIVvolt={IVvolt}, IVamps= {IVamps}, IVwatt={IVwatt}, IVison={IVison}")


# form a data record
body_solar = [
    {
        "measurement": measurement_name,
        "time": timestamp,
        "fields": {
            "PVvolt": PVvolt,
            "PVamps": PVamps,
            "PVwatt": PVwatt,
            "PVkwh": up.readReg(PVkwhTotal),
            "PVkwh2d": up.readReg(PVkwhToday),
            "BAvolt": up.readReg(BAvolt),
            "BAamps": up.readReg(BAamps) + FloatNo,
            "BAperc": up.readReg(BAperc),
            "DCvolt": DCvolt,
            "DCamps": DCamps,
            "DCwatt": DCwatt,
            "DCkwh": up.readReg(DCkwhTotal),
            "DCkwh2d": up.readReg(DCkwhToday),
            "IVvolt": IVvolt,
            "IVamps": IVamps,
            "IVwatt": IVwatt,
            "IVison": IVison,
        }
    }
]

print (body_solar)

# connect to influ
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
# write the measurement
ifclient.write_points(body_solar)
