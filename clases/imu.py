import drivers.mpu6050 as mpu
import drivers.constants as reg
import ustruct, uos
from machine import Pin

class IMU(object):
	"""
	Clase para la interacción sencilla con el periférico MPU6050
	TO DO
		- implementar reseteo de la fifo
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
		#text += "\n"
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
	"""def writesamples(self, duration=5, samplingrate=10):
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
	"""
	def setsamplerate(self, fs):
		"""
		La frecuencia de muestreo puede ir entre 4 Hz y 1 kHz
		esto, dejando el DLPF_CFG del registro 26 distinto de 0 o 7
		"""
		old = self.imu.read_byte(reg.MPU6050_RA_CONFIG)
		self.imu.write_byte(reg.MPU6050_RA_CONFIG, (old & 0b11111000) | 1)
		if fs >= 4 and fs <= 1000:
			samplingrate = fs
		elif fs > 1000:
			samplingrate = 1000
		else:
			samplingrate = 4
		SMPLRT_DIV = int(1e3 / samplingrate - 1)
		self.imu.write_byte(reg.MPU6050_RA_SMPLRT_DIV, SMPLRT_DIV)

	def setscale(self, acc_scale, gyro_scale):
		"""
		Ajusta la escala del acelerometro entre +-2g y +-16g
		acc_scale = 0 -> +- 2g
		acc_scale = 1 -> +- 4g
		acc_scale = 2 -> +- 8g
		acc_scale = 3 -> +- 16g
	
		Ajusta la escala del giroscopio entre +-250°/s y +-2000°/s
		gyro_scale = 0 -> +- 250°/s
		gyro_scale = 1 -> +- 500°/s
		gyro_scale = 2 -> +- 1000°/s
		gyro_scale = 3 -> +- 2000°/s

		"""
		pass
		#self.imu.(reg.MPU6050_RA_ACCEL_CONFIG, )

	def dumpfifo(self):
		"""
		Permite leer en rafaga los bytes albergados en la FIFO, retorna un bytearray
		"""
		fifoenabled   = self.imu.read_byte(reg.MPU6050_RA_FIFO_EN)
		bytesread = bytearray()
		if fifoenabled is 0:
			return bytesread
		fifocount 	  = self.fifo_count()
		for i in range(fifocount):
			bytesread.append(self.imu.read_byte(reg.MPU6050_RA_FIFO_R_W))
		return bytesread

	def sortfifo(self, buf):
		"""
		Distribuye los datos crudos de la fifo en una lista de acuerdo al orden
		acordado en el laboratorio:
		Cada muestra tiene 8 bytes
		Primero en salir |	2B	|	2B	|	2B	|	2B	| Ultimo en salir
						   temp   acelX   acelY   acelZ
		"""
		samples = []
		for x in range(0, len(buf), 8):
			samples.append(ustruct.unpack('>hhhh', buf[x:x+8]))
		return samples

	def fifo_enable(self):
		# metodo para direccionar las muestras de los sensores hacia la fifo
		# Registro 35 (FIFO_EN)
		# MPU6050_RA_FIFO_EN = 0x23
		# y Registro 106 (USER_CTRL)
		# MPU6050_RA_USER_CTRL = 0x6A
		old = self.imu.read_byte(0x6A)
		# FIFO RESET
		self.imu.write_byte(0x6A, old & 0b10111111) # se desactiva FIFO ENABLE para hacer el reset
		self.imu.write_byte(0x6A, old | 0b00000100)

		self.imu.write_byte(0x23, 0b10001000) # escribiendo 0b10001000 se leen 2B temp + 6B acel
		# FIFO ENABLE 
		self.imu.write_byte(0x6A, old | 0b01000000)

	def fifo_count(self):
		# este metodo lee el registro 114 (FIFO_COUNT)
		# este registro lleva la cuenta de las muestras actualmente en la fifo
		# falta convertir el numero a su valor real
		count = ustruct.unpack('>h',bytearray([self.imu.read_byte(0x72), self.imu.read_byte(0x73)]))
		return count[0]

	def irq_enable(self):
		# activa la interrupcion del registro 56 (INT_ENABLE)
		#MPU6050_RA_INT_ENABLE                 = 0x38
		self.imu.write_byte(0x38, 0b00010000)

	def irq_status(self):
		return self.imu.read_byte(0x3A)

	def int_umbral(self, umbral, tiempo):
		# Configura el umbral y el tiempo de la ventana para la interrupcion por umbral
		# El tiempo esta en segundos y el umbral en g
		self.imu.set_motion_detection_threshold(threshold=umbral)
		self.imu.set_motion_detection_duration(duration=tiempo)
		self.imu.set_int_motion_enabled(enabled=True)
		print('Deteccion por umbral ready')
