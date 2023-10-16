#!/usr/bin/python3

from influxdb import InfluxDBClient
from SolarTracer import *
from InfluxConf import *

measurement_name = "solar_stats"
tracer = SolarTracer(debug=0)

try:
    body_stats = [
        {
            "measurement": measurement_name,
            "time": tracer.getTimestamp(),
            "fields": tracer.readStats()
        }
    ]
except IOError:
    print("Could not obtain measurements from", tracer, file=sys.stderr)
else:
    print (body_stats)
    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)
    # write the measurement
    ifclient.write_points(body_stats)

