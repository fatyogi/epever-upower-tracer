#!/usr/bin/python3

import sdm_modbus

def readsdm230(DEVICE="/dev/ttyXRUSB1",UNIT=1, debug=0) -> dict:
    
    meter = sdm_modbus.SDM230(device=DEVICE,stopbits=1,parity="N",baud=9600,timeout=1,unit=UNIT)
    if (meter.connected() == False):
        print(f"Connection to {DEVICE}({UNIT}) failed")
        return {}
    sdm = {"IVon": 0}
    # read the data
    try:
        regs = meter.read_all(sdm_modbus.registerType.INPUT)
        if debug>0: print("Registers:", regs)
    except IOError:
        print("Unable to read from %s(%d)" % (DEVICE, UNIT))
    else:
        if regs == {}:
            return {}
        idx = 0
        for k, v in regs.items():
            address, length, rtype, dtype, vtype, label, fmt, batch, sf = meter.registers[k]
            if debug>0: print(f"{label} = {k} --> {v:.2f}{fmt}")
            if (idx < 8):
                sdm[k] = round(v, 4)
            idx += 1
        sdm["IVon"] = 1
    return sdm
