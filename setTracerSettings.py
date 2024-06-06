#!/usr/bin/python3
from SolarTracer import *
from InfluxConf import *

# connect to the Tracer
tracer = SolarTracer(TRACER_PORT, debug=0)
print (tracer)

# Display current settings
print ("\n==> Current battery settings are: ")
tracer.printBatterySettings()

# MODIFY THE LINE BELOW TO MATCH YOUR BATTERY PARAMETERS, for example:
#
# Use tracer.setBatterySettings(batteryLiFePO4, 300) to set a 12V LiFePO4 battery of 300 Ah capacity
# Use tracer.setBatterySettings(batteryLiFePO4, 500, 24) to set a 24V LiFePO4 battery of 500 Ah capacity
# Use tracer.setBatterySettings(batteryLeadAcid, 200, 12) to set a 12V LeadAcid battery of 200 Ah capacity

tracer.setBatterySettings(batteryLiFePO4, 160)

# Verify new settings
print ("\n==> The new settings are: ")
tracer.printBatterySettings()
