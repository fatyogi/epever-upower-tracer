#!/usr/bin/python
import datetime
import time
from influxdb import InfluxDBClient
from UPower import *

# influx configuration - edit these
ifuser = "grafana"
ifpass = "solar"
ifdb   = "solar"
ifhost = "127.0.0.1"
ifport = 8086
measurement_name = "solar"


up = UPower()
if (up.connect() < 0):
	print("Could not connect to the device")
	exit -2

# get timestamps
localtime = time.localtime()
timestamp = time.strftime("%H:%M:%S", localtime)
timestamp = datetime.datetime.utcnow()

# form a data record
body_solar = [
    {
        "measurement": measurement_name,
        "time": timestamp,
        "fields": {
            "PVvolt": up.readReg(PVvolt),
            "PVamps": up.readReg(PVamps),
            "PVwatt": up.readReg(PVwattL),
            "PVkwh": up.readReg(PVkwhL),
            "PVtemp": up.readReg(PVtemp),
            "BAvolt": up.readReg(BAvolt),
            "BAamps": up.readReg(BAamps),
            "BAwatt": up.readReg(BAwattL),
            "BAah": up.readReg(BAah),
            "BAtemp": up.readReg(BAtemp),
            "ACvoltIN": up.readReg(ACvoltIN),
            "ACvolt": up.readReg(ACvolt),
            "ACamps": up.readReg(ACamps),
            "ACwatt": up.readReg(ACwattL),
            "ACtemp": up.readReg(ACtemp),
            "IVwattL": up.readReg(IVwattL),
            "IVwattH": up.readReg(IVwattH),
            "IVherz": up.readReg(IVherz),
            "IVvoltIN": up.readReg(IVvoltIN),
            "IVvolt": up.readReg(IVvolt),
            "IVamps": up.readReg(IVamps),
            "IVstat": up.getIV(),
            "ACstat": up.getAC()
        }
    }
]

print(body_solar)

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
# write the measurement
ifclient.write_points(body_solar)
