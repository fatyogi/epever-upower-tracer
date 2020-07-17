import minimalmodbus

# on/off
ON = 1
OFF = 0

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
	def readReg(self,register):
	    try:
	            reading = self.instrument.read_register(register, 2, 4)
	            return reading
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
    			print "Could not convert data!"
    			return -3



