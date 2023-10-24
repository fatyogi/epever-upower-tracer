#!/usr/bin/python3

from InfluxConf import *
from SolarTracer import *
from sdm230 import *

# connect to the Tracer
tracer = SolarTracer(TRACER_PORT, debug=0)

# connect to Influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# Reading the Tracer
try:
    body_solar = [
        {
            "measurement": "solar",
            "time": tracer.getTimestamp(),
            "fields": tracer.readCurrent()
        }
    ]
except IOError:
    print("Could not obtain measurements from", tracer, file=sys.stderr)
else:
    print (body_solar)
    # write the measurement
    ifclient.write_points(body_solar)

######### Reading the SDM (AC data) ###########
try:
    acpower = readsdm230(SDM_PORT)
except IOError:
    print("Could not obtain measurements from SDM230", file=sys.stderr)
else:
    if (acpower != {}):
        body_acpower = [
            {
                "measurement": "acpower",
                "time": tracer.getTimestamp(),
                "fields": acpower
            }
        ]
        print (body_acpower)
        # write the measurement
        ifclient.write_points(body_acpower)

