import drivers.mpu6050 as mpu
import drivers.constants as reg
import ustruct
from machine import Pin
from uos import *
from utime import *

class IMU(object):
	"""
	Clase para la interacción sencilla con el periférico MPU6050
	"""
	fileCounter = 0
	try:
		f = open("fileCounterIMU.txt", "r")
		fileCounter = int(f.read())
		print(fileCounter)
		f.close()
	except OSError:
		f = open("fileCounterIMU.txt", "w")
		f.write("0")
		f.close()
		fileCounter = 0 



	def __init__(self):
		super(IMU, self).__init__()
		self.vext_pin = Pin(21, Pin.OUT, value = 0)
		self.imu = mpu.MPU()
		self.counter = 0
		self.sd = None
		#self.reset_registers()

	# Lectura escalada de los sensores en formato:
	# [acc_x, acc_y, acc_z, temp_raw, gyro_x, gyro_y, gyro_z]
	def scaledread(self):
		return self.imu.read_sensors_scaled()

	# Convierte un iterable (lista o tupla) en una fila en formato csv (texto)
	def readtostring(self, read):
		x = read
		text = ""
		for _x in x:
			text += str(_x)+","
		text += "\n"
		return text

	# Cambia el estado del chip, True = dormido, False = despierto
	# Usa el registro MPU6050_RA_PWR_MGMT_1 = 0x6B
	# TODO: muy rudimentario, mejorar codigo
	def setsleep(self, state):
		state = 1 if state is True else 0
		bitToChange = int(b'0100_0000',2)
		value = self.imu.read_byte(reg.MPU6050_RA_PWR_MGMT_1)
		self.imu.write_byte(reg.MPU6050_RA_PWR_MGMT_1, value | ((state << 6) & bitToChange))
		return True if (self.imu.read_byte(reg.MPU6050_RA_PWR_MGMT_1) & bitToChange) >> 6 is state else False 

	# Vuelve todos los registros del chip a su estado original
	# (ver el mapa de registros para más info)
	def resetregisters(self):
		self.imu.write_byte(reg.MPU6050_RA_PWR_MGMT_1, int(b'1000_0000',2))

	# Se puede añadir una tarjeta SD para escribir a un archivo
	def attachSD(self, sd):
		self.sd = sd
	
	# Se escribe el contenido de "data" a la tarjeta sd añadida previamente
	# Devuelve una tupla con la cantidad de bytes y lineas escritas 
	# (bytes_writen, lines_writen)
	def writeSD(self, filename, data):
		pass

	# Reinicia el contador que sirve para diferenciar un archivo de otro
	# TODO: muy rudimentario, mejorar este sistema de guardado
	def resetcounter(self):
		f = open("fileCounterIMU.txt",'w')
		f.write("0")
		f.close()

	# Saca una muestra cada 1/samplingrate de los registros de los sensores
	# (obsoleto)
	# TODO: mejorar o eliminar este metodo
	def writesamples(self, duration=5, samplingrate=10):
		if self.sd is not None:
			IMU.fileCounter += 1
			fc = open("fileCounterIMU.txt", "w")
			print(str(IMU.fileCounter))
			fc.write(str(IMU.fileCounter))
			fc.close()
			mount(self.sd, "/")
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
					x = self.scaledread()
					saved = False
					check = ticks_us()
				elif not saved:
					numwrite += f.write(self.readtostring(x))
					saved = True
			print("bytes escritos: "+str(numwrite))
			f.close()
			umount("/")
	
	#Permite leer en rafaga los bytes albergados en la FIFO, retorna un bytearray
	def dumpfifo(self):
		fifoenabled   = self.imu.read_byte(reg.MPU6050_RA_FIFO_EN)
		if fifoenabled is 0:
			return bytearray()
		fifocount 	  = self.fifo_count()
		bytesread 	  = bytearray()
		for i in xrange(fifocount):
			bytesread.append(self.imu.read_byte(reg.MPU6050_RA_FIFO_R_W))
		return bytesread

	def fifo_enable(self):
		# metodo para direccionar las muestras de los sensores hacia la fifo
		# Registro 35 (FIFO_EN)
		# MPU6050_RA_FIFO_EN = 0x23
		self.imu.write_byte(0x23, 128)

	def fifo_count(self):
		# este metodo lee el registro 114 (FIFO_COUNT)
		# este registro lleva la cuenta de las muestras actualmente en la fifo
		# falta convertir el numero a su valor real
		count = ustruct.unpack('>h',bytearray([self.imu.read_byte(0x72) self.imu.read_byte(0x73)]))
		return count[0]

	def irq_enable(self):
		# activa la interrupcion del registro 56 (INT_ENABLE)
		#MPU6050_RA_INT_ENABLE                 = 0x38
		# se deja en 1 para activar solo DATA_RDY_EN
		self.imu.write_byte(0x38, 1)

	def irq_status(self):
		return self.imu.read_byte(0x3A)

