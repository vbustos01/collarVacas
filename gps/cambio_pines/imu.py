import drivers.mpu6050 as mpu
import _thread as thread
from machine import Pin
from uos import *
from utime import *

class IMU(object):
	"""docstring for IMU"""

	PWR_MGMT1_REG = 0x6B
	PWR_MGMT2_REG = 0x6C
	fileCounter = 0

	def __init__(self):
		super(IMU, self).__init__()
		self.vext_pin = Pin(21, Pin.OUT, value = 0)
		self.imu = mpu.MPU()
		self.counter = 0
		self.isThreadActive = False
		self.sd = None
		#self.reset_registers()

	def rawread(self):
		return self.imu.read_sensors_scaled()

	def readtostring(self, read):
		x = read
		text = ""
		for _x in x:
			text += str(_x)+","
		text += "\n"
		return text

	def setsleep(self, state):
		state = 1 if state is True else 0
		bitToChange = int(b'0100_0000',2)
		value = self.imu.read_byte(IMU.PWR_MGMT1_REG)
		self.imu.write_byte(IMU.PWR_MGMT1_REG, value | ((state << 6) & bitToChange))
		return True if (self.imu.read_byte(IMU.PWR_MGMT1_REG) & bitToChange) >> 6 is state else False 

	def resetregisters(self):
		self.imu.write_byte(IMU.PWR_MGMT1_REG, int(b'1000_0000',2))

	def attachSD(self, sd):
		self.sd = sd

	def writesamples(self, duration=5, samplingrate=10):
		if self.sd is not None:
			mount(self.sd, "/")
			IMU.fileCounter += 1
			f = open("imu"+str(IMU.fileCounter)+".csv","w")
			print("nombre archivo: imu"+str(IMU.fileCounter)+".csv")
			now = ticks_ms()
			check = ticks_us()
			samplingperiod = 1E6/samplingrate
			print("periodo de muestreo: "+str(samplingperiod))
			numwrite = 0
			saved = True
			x = None
			while ticks_diff(ticks_ms(), now) < (duration*1000):
				if ticks_diff(ticks_us(), check) >= samplingperiod:
					x = self.rawread()
					saved = False
					check = ticks_us()
				elif not saved:
					numwrite += f.write(self.readtostring(x))
					saved = True
			print("bytes escritos: "+str(numwrite))
			f.close()
			umount("/")