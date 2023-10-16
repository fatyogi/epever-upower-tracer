#!/usr/bin/python3
from SolarTracer import *

tracer = SolarTracer(debug=1)
print (tracer)

# Display current settings
tracer.printBatterySettings()

# Use setBatterySettings(batteryLiFePO4, 300) to set a 12V LiFePO4 battery of 300 Ah capacity
# Use setBatterySettings(batteryLiFePO4, 500, 48) to set a 24V LiFePO4 battery of 500 Ah capacity
tracer.setBatterySettings(batteryLiFePO4, 160)

# Verify new settings
tracer.printBatterySettings()
