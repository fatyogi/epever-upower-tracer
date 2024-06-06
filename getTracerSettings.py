#!/usr/bin/python3
from SolarTracer import *
from InfluxConf import *

# connect to the Tracer
tracer = SolarTracer(TRACER_PORT, debug=0)
print (tracer)

# Display current settings
print ("\n==> Current battery settings are: ")
tracer.printBatterySettings()

