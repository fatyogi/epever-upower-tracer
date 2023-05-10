#!/usr/bin/python3

import sdm_modbus


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
    IVon = True

    # read the data
    regs = meter.read_all(sdm_modbus.registerType.INPUT)
    if (regs == {}): IVon=False
    else:
        for k, v in regs.items():
            address, length, rtype, dtype, vtype, label, fmt, batch, sf = meter.registers[k]
            print(f"{label} = {k} --> {v:.2f}{fmt}")
            if k == "voltage": IVvolt=round(v,2)
            if k == "current": IVamps=round(v,2)
            if k == "power_active": IVamps=round(v,2)

    return (IVvolt,IVamps,IVwatt,IVon)


(IVvolt,IVamps,IVwatt,IVon) = readsdm230()

print (f"\nIVvolt={IVvolt}, IVamps= {IVamps}, IVwatt={IVwatt}, IVon={IVon}")
