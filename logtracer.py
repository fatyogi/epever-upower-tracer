#!/usr/bin/python3

from influxdb import InfluxDBClient
from SolarTracer import *
from InfluxConf import *

# connect to the Tracer
tracer = SolarTracer(TRACER_PORT, debug=0)
measurement_name = "solar"

try:
    body_solar = [
        {
            "measurement": measurement_name,
            "time": tracer.getTimestamp(),
            "fields": tracer.readCurrent()
        }
    ]
except IOError:
    print("Could not obtain measurements from", tracer, file=sys.stderr)
else:
    print (body_solar)
    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
    # write the measurement
    ifclient.write_points(body_solar)
