# This package is now supported under Python 3

import minimalmodbus

# on/off
ON = 1
OFF = 0

# Float conversion for Python 3
FloatConv = 0.0

# PV array
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

# DC load
DCvolt = 0x310C
DCamps = 0x310D
DCwattL = 0x310E
DCwattH = 0x310F

# Statistics
PVkwhTotal = 0x3312
DCkwhTotal = 0x330A
PVkwhToday = 0x330C
DCkwhToday = 0x3304

ControllerTemp = 0x3111

# Settings
BatteryType=0x9000
BatteryCapacity=0x9001
TempCompensationCoeff=0x9002
OverVoltageDisconnect=0x9003
ChargingLimitVoltage=0x9004
OverVoltageReconnect=0x9005
EqualizationVoltage=0x9006
BoostVoltage=0x9007
FloatVoltage=0x9008
BoostReconnectVoltage=0x9009
LowVoltageReconnect=0x900A
UnderVoltageRecover=0x900B
UnderVoltageWarning=0x900C
LowVoltageDisconnect=0x900D
DischargingLimitVoltage=0x900E
# Load settings
LoadControlMode=0x903D
LoadControlModes = ["Manual Control", "Light ON/OFF", "Light ON+ Timer", "Time Control"]
LoadManualStatus = 0x906A

settingsRegBlockStart = 36864
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
##### Use setBatterySettings(batteryLiFePO4, 300) to set a 12V LiFePO4 battery of 300 Ah capacity
##### Use setBatterySettings(batteryLiFePO4, 500, 48) to set a 24V LiFePO4 battery of 500 Ah capacity

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
	"""A member of SolarTracer communication class."""

	# connect to device
	def __init__(self, device = '/dev/ttyXRUSB0', serialid = 1):
		self.device = device
		self.id = serialid
		self.instrument = 0


	def connect(self):
	    try:
	            self.instrument = minimalmodbus.Instrument(self.device, self.id)
	    except minimalmodbus.serial.SerialException:
	            return -1

	    self.instrument.serial.baudrate = 115200
	    self.instrument.serial.bytesize = 8
	    self.instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
	    self.instrument.serial.stopbits = 1
	    self.instrument.serial.timeout  = 1.2
	    self.instrument.mode = minimalmodbus.MODE_RTU
	    return 0

	# read informational register
	def readReg(self,register) -> float:
	    try:
	            reading = self.instrument.read_register(register, 2, 4)
	            return (reading + FloatConv)
	    except IOError:
	            return -2

	# read parameter
	def readParam(self,register,decimals=2,func=3):
	    try:
	            reading = self.instrument.read_register(register, decimals, func)
	            return reading
	    except IOError:
	            return -2

	# write parameter
	def writeParam(self,register,value,decimals=2,func=16):
	    try:
	            reading = self.instrument.write_register(register, value, decimals, func)
	            return 0
	    except IOError as err:
	    		return -2
	    except ValueError:
    			print ("Could not convert data!")
    			return -3

	
	################# Status & Settings ###############
	def statLoad(self, newStatus = -1, decimals=0,func=3):
		if (newStatus > 0):
			try:
				self.writeParam(LoadManualStatus, newStatus)
			except IOError:
				return -3
		try:
			reading = self.instrument.read_register(LoadManualStatus, decimals, func)
			return reading
		except IOError:
			return -2

	### Output battery settings to the console (temp. coefficient omitted)
	def printBatterySettings(self):
		settingsReg = []
		try:
			settingRegs = self.instrument.read_registers(settingsRegBlockStart, settingsRegBlockLength)
		except IOError:
			return -2

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
			idx = idx + 1

	### Set battery settings
	def setBatterySettings(self, settingsList, batteryCapacity=100, batteryVoltage=12):
		### WRITE MULTIPLE REGISTERS
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
			self.instrument.write_registers(settingsRegBlockStart, newSettings)
			return 0
		except IOError:
			return -2





