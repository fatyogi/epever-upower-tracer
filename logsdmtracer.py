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

def readsdm230( DEVICE="/dev/ttyXRUSB1",STOPBITS=1,PARITY="N",BAUD=9600,TIMEOUT=1,UNIT=1 ):
    meter = sdm_modbus.SDM230 (
                device=DEVICE,
                stopbits=STOPBITS,
                parity=PARITY,
                baud=BAUD,
                timeout=TIMEOUT,
                unit=UNIT
            )
    IVvolt = 0.0
    IVamps = 0.0
    IVwatt = 0.0
    IVison = 1
    # read the data
    regs = meter.read_all(sdm_modbus.registerType.INPUT)
    if (regs == {}): IVison=0
    else:
        for k, v in regs.items():
            address, length, rtype, dtype, vtype, label, fmt, batch, sf = meter.registers[k]
# Uncomment for debugging
#            print(f"{label} = {k} --> {v:.2f}{fmt}")
            if k == "voltage": IVvolt=round(v,2)
            if k == "current": IVamps=round(v,2)
            if k == "power_active": IVwatt=round(v,2)
    # Sometimes the meter returns a weird value of 12000 watt or over, which messes up the graph. Blocking that behaviour.
    if (IVwatt > 5000): IVwatt = 0.0;
    return (IVvolt,IVamps,IVwatt,IVison)


(IVvolt,IVamps,IVwatt,IVison) = readsdm230()

# Uncomment for debugging
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
