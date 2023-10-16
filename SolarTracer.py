# Full rewrite of SolarTracer.py for Python3
# No ugly int to float conversions
# Reading multiple registers into dict
# The module is aware of the registers

# readCurrent() and readStats() are two separate methods
# that return all necessary values

import sys
import datetime
import time
import minimalmodbus

#### Current values registers ####
PVvolt = 0x3100
PVamps = 0x3101
PVwattL = 0x3102
PVwattH = 0x3103
PVstat = 0x3201

# battery
BAvolt = 0x3104
BAamps = 0x3105
BAwattL = 0x3106
BAwattH = 0x3107
BAtemp = 0x3110
BAperc = 0x311A
BAstat = 0x3200
BAcurL = 0x331B
BAcurH = 0x331C


# DC load
DCvolt = 0x310C
DCamps = 0x310D
DCwattL = 0x310E
DCwattH = 0x310F

#### Statistics registers ####
PVkwhTotal = 0x3312
DCkwhTotal = 0x330A
PVkwhToday = 0x330C
DCkwhToday = 0x3304

###### Battery settings ######
settingsRegBlockStart = 0x9000
settingsRegBlockLength = 15
tracerSettingsNames = ["BatteryType", 
                "BatteryCapacity",
                "TempCompensationCoefficient", 
                "HighVoltageDisconnect", 
                "ChargingLimitVoltage", 
                "OverVoltageReconnect",
                "EqualizationVoltage",
                "BoostVoltage",
                "FloatVoltage",
                "BoostReconnectVoltage",
                "LowVoltageReconnect",
                "UnderVoltageReconnect",
                "UnderVoltageWarning",
                "LowVoltageDisconnect",
                "DischargingLimitVoltage"]

tracerBatteryType = ["USER","SEALED","GEL","FLOODED"]

##### Battery settings for a type (12V)
##### Source: Victron Energy Manual 

batteryLeadAcid = [
    0x0,  # (0x9000 = 0000H - User defined)
    300, # (0x9001 = 300AH - Battery Capacity)
    300, # (0x9002 = 3.00mV/C/2V - Temperature compensationcoefficient)
    1620, # (0x9003 = 16.20V - High Volt.disconnect)
    1500, # (0x9004 = 15.00V - Charging limit voltage)
    1500, # (0x9005 = 15.00V - Over voltage reconnect)
    1460, # (0x9006 = 14.60V - Equalization voltage)
    1440, # (0x9007 = 14.40V - Boost voltage)
    1380, # (0x9008 = 13.80V - Float voltage)
    1630, # (0x9009 = 16.30V - Boost reconnect voltage)
    1260, # (0x900A = 12.60V - Low voltage reconnect)
    1220, # (0x900B = 12.20V - Under voltage recover)
    1200, # (0x900C = 12.00V - Under voltage warning)
    1110, # (0x900D = 11.10V - Low voltage disconnect)
    1060, # (0x900E = 10.60V - Discharging limit voltage)
]

batteryLiFePO4 = [
    0x0,  # (0x9000 = 0000H - User defined)
    300, # (0x9001 = 300AH - Battery Capacity)
    300, # (0x9002 = 3.00mV/C/2V - Temperature compensationcoefficient)
    1500, # (0x9003 = 15.00V - High Volt.disconnect)
    1460, # (0x9004 = 14.60V - Charging limit voltage)
    1420, # (0x9005 = 14.20V - Over voltage reconnect)
    1400, # (0x9006 = 14.00V - Equalization voltage)
    1380, # (0x9007 = 13.80V - Boost voltage)
    1380, # (0x9008 = 13.80V - Float voltage)
    1320, # (0x9009 = 13.20V - Boost reconnect voltage)
    1240, # (0x900A = 12.40V - Low voltage reconnect)
    1200, # (0x900B = 12.00V - Under voltage recover OR Under voltage Warning Reconnect)
    1160, # (0x900C = 11.60V - Under voltage warning)
    1080, # (0x900D = 10.80V - Low voltage disconnect)
    1040, # (0x900E = 10.40V - Discharging limit voltage)
]

class SolarTracer:
    """Class representing a Tracer device"""

    # Solar Tracer constructor
    def __init__(self, device = '/dev/ttyXRUSB0', serialid = 1, debug = 0):
        self.device = device
        self.id = serialid
        self.debug = debug

        try:
            instrument = minimalmodbus.Instrument(self.device, self.id)
            if (self.debug>0):
                print("DEBUG: successfully connected to", self.device)
            
            # set instrument Serial settings
            instrument.serial.baudrate = 115200
            instrument.serial.bytesize = 8
            instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 2
            instrument.mode = minimalmodbus.MODE_RTU
            instrument.debug = False

            self.instrument = instrument
            self.connected = True

        except IOError:
            self.connected = False
            print("ERROR: Failed to connect to", self.device, file=sys.stderr)
            sys.exit(1)

    # Solar Tracer destructor
    def __del__(self):
        """Destruct the SolarTracer object"""
        if self.connected:
            self.instrument.serial.close()
            if self.debug>0: print("DEBUG: successfully disconnected", self.device)

    # String representation of a controller
    def __str__(self) -> str:
        stat = "disconnected"
        if self.connected: stat = "connected"
        return f"{self.device}({self.id}): {stat}"
    
    # Get current timestamp
    def getTimestamp(self):
        """Get current timestamp from the system"""
        localtime = time.localtime()
        localstamp = time.strftime("%H:%M:%S", localtime)
        timestamp = datetime.datetime.utcnow()
        if self.debug > 0: print ("DEBUG: Local time", localstamp, ", UTC timestamp", timestamp)
        return timestamp
    
    # Read Register
    def readReg(self,register) -> float:
        """Read a float register from the Tracer"""
        try:
            value = float(self.instrument.read_register(register, 2, 4))
            if self.debug > 0: print ("DEBUG: Successfully read from 0x%X" % register)
            return value
        except IOError:
            print("ERROR: Failed to read from 0x%X" % register, file=sys.stderr)
            return -1

    ### Output battery settings to the console (temp. coefficient omitted)
    def printBatterySettings(self):
        """Read battery settings and print out"""
        settingRegs = self.instrument.read_registers(settingsRegBlockStart, settingsRegBlockLength)
        idx = 0
        for param in settingRegs:
            if (idx == 0):
                print ("{:<25}: {:<4}({:<1})".format(tracerSettingsNames[idx], tracerBatteryType[idx], param))
            elif (idx == 1):
                print ("{:<25}: {:<4}Ah".format(tracerSettingsNames[idx], param))
            elif (idx == 2):
                next
            else:
                print ("{:<25}: {:.1f}".format(tracerSettingsNames[idx], float(param)/100))
            idx += 1

    ### Set battery settings
    def setBatterySettings(self, settingsList, batteryCapacity=100, batteryVoltage=12) -> int:
        """Set battery setting by writing multiple registers"""
        """Use setBatterySettings(batteryLiFePO4, 300) to set a 12V LiFePO4 battery of 300 Ah capacity"""
        """Use setBatterySettings(batteryLiFePO4, 500, 48) to set a 24V LiFePO4 battery of 500 Ah capacity"""
        newSettings = settingsList
        if (batteryCapacity != 100):
            newSettings[1] = batteryCapacity
        if (batteryVoltage > 12):
            voltAdjust = batteryVoltage / 12
            idx = 0
            for voltage in newSettings:
                if (idx > 2):
                    newSettings[idx] = newSettings[idx] * voltAdjust
                idx = idx + 1
        # write all settings to the controller
        try:
            if self.debug>0: print ("DEBUG: Writing new settings to %s(%d)" % (self.device, self.id))
            self.instrument.write_registers(settingsRegBlockStart, newSettings)
            return 0
        except IOError:
            if self.debug>0: print ("DEBUG: failed writing settings to %s!" % self.device)
            return -2
            

    def readCurrent(self) -> dict:
        tracerCurrent = {}
        regs = []
        
        # Reading the block of current value registers
        blk = 0x3100
        numreg = 0x12
        if self.debug>0: print("DEBUG reading %d registers starting at 0x%X from %s" % (numreg, blk, self.device))
        try:
            regs = self.instrument.read_registers(blk, numreg, 4)
            if self.debug>0: print ("DEBUG Registers:", regs)
        except IOError:
            print("Failed to read %d registers at 0xX from %s" % (numreg, blk1, self.device), file=sys.stderr)
            return []

        tracerCurrent = {
                "PVvolt": regs[0]/100.0,
                "PVamps": regs[1]/100.0,
                "PVwatt": regs[2]/100.0, # round((regs[0]/100)*(regs[1]/100),2)
                # reg[3] contains high bits of PVwatt, which are not currently processed
                "BAvolt": regs[4]/100.0,
                "BAamps": regs[5]/100.0,
                "BAwatt": regs[6]/100.0, # round((regs[4]/100)*(regs[5]/100),2)
                # reg[7] contains high bits of BAwatt, which are not currently processed
                # reg[8], reg[9], reg[0xA], reg[0xB] - empty for now
                "DCvolt": regs[0xC]/100.0,
                "DCamps": regs[0xD]/100.0,
                "DCwatt": regs[0xE]/100.0,
                # reg[0xF] contains high bits of DCwatt, which are not currently processed
                "BAtemp": regs[0x10]/100.0,
                "CTtemp": regs[0x11]/100.0,
                }
        
        # additional registers here
        # read the isolated "battery" registers
        BApc = self.readReg(BAperc)
        if BApc>0:
            addic = {"BAperc": BApc*100}
            tracerCurrent.update(addic)
        BAcr = self.readReg(BAcurL)
        if BAcr>0:
            addic = {"BAcurr": round(BAcr/100.0,4)}
            tracerCurrent.update(addic)

        return tracerCurrent

    def readStats(self) -> dict:
        tracerStats = {}
        regs = []
        blk = 0x3300
        numreg = 0x3314-blk
        if self.debug>0: print("DEBUG reading %d registers starting at 0x%X from %s" % (numreg, blk, self.device))
        try:
            regs = self.instrument.read_registers(blk, numreg, 4)
            if self.debug>0: print ("DEBUG Registers:", regs)
        except IOError:
            print("Failed to read %d registers at 0xX from %s" % (numreg, blk1, self.device), file=sys.stderr)
            return []
        else:
            tracerStats = {
                "DCkwh2d" : regs[0x04]/100.0, # KWH consumed today L
                "DCkwhTm" : regs[0x06]/100.0, # KWH consumed this month L
                "DCkwhTY" : regs[0x08]/100.0, # KWH consumed this year (from 01 Jan) L
                "DCkwhTT" : regs[0x0a]/100.0, # KWH consumed TOTAL L
                "PVkwh2d" : regs[0x0c]/100.0, # KWH generated today L
                "PVkwhTm" : regs[0x0e]/100.0, # KWH generated this month L
                "PVkwhTY" : regs[0x10]/100.0, # KWH generated this year (from 01 Jan) L
                "PVkwhTT" : regs[0x12]/100.0, # KWH consumed TOTAL L
            }
            return tracerStats
        
