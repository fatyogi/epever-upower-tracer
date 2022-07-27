#!/usr/bin/python
import sys
import datetime
import time
import minimalmodbus
from influxdb import InfluxDBClient
from SolarTracer import *

# influx configuration - edit these
ifuser = "grafana"
ifpass = "solar"
ifdb   = "solar"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "solar"


up = SolarTracer()
if (up.connect() < 0):
	print("Could not connect to the device")
	exit -2

# get timestamps
localtime = time.localtime()
timestamp = time.strftime("%H:%M:%S", localtime)
timestamp = datetime.datetime.utcnow()

# calculate compound values
PVwatt = up.readReg(PVwattH)
PVwatt = ((int(PVwatt) << 16) + up.readReg(PVwattL));
DCwatt = up.readReg(DCwattH)
DCwatt = ((int(DCwatt) << 16) + up.readReg(DCwattL));

# form a data record
body_solar = [
    {
        "measurement": measurement_name,
        "time": timestamp,
        "fields": {
            "PVvolt": up.readReg(PVvolt),
            "PVamps": up.readReg(PVamps),
            "PVwatt": PVwatt,
            "PVkwh": up.readReg(PVkwhTotal),
            "PVkwh2d": up.readReg(PVkwhToday),
            "BAvolt": up.readReg(BAvolt),
            "BAamps": up.readReg(BAamps),
            "BAperc": up.readReg(BAperc),
            "DCvolt": up.readReg(DCvolt),
            "DCamps": up.readReg(DCamps),
            "DCwatt": DCwatt,
            "DCkwh": up.readReg(DCkwhTotal),
            "DCkwh2d": up.readReg(DCkwhToday),
        }
    }
]

print(body_solar)

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
# write the measurement
ifclient.write_points(body_solar)
