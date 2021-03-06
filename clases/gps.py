#!/usr/bin/env python
# objeto gps del cual se puede extraer info sobre la posicion
# ademas inicializa la comunicacion via UART con el gps

from machine import UART
from time import sleep, ticks_diff, ticks_ms
from uos import *

class GPS():
	"""
		Modulo gps
		
		Clase encargada de inicializar el modulo gps para la operacion
		en una ESP32

		TODO:
			- Crear un archivo de configuracion para distintos modos de operacion
	"""
	def __init__(self):
		self.uart = UART(2, 9600)
		self.uart.init(9600, bits=8, parity=None, stop=2, tx=33, rx=17)
		self.pos = 0
		# configurar gps a 9600 baud
		#self.uart.write(b'$PMTK251,9600*27\r\n')

	def write2sd(self, timeout):
	# Metodo utilizado para obtener y guardar la posicion actual en la sd
		self.uart.write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')
		sleep(1)
		timestart = ticks_ms()
		while ticks_diff(ticks_ms(), timestart) < timeout:
		# iteracion para asegurar la posicion correcta
		# en caso de superar el timeout graba el texto posicion indeterminada
			self.frame = self.uart.readline()
			self.pos = str(self.frame).split(',')
			try:
				if self.pos[2]=='A':
					break
			except IndexError:
				# si la cadena esta vacia la informacion tambien es invalida
				continue
			except:
				print('error desconocido')

		if ticks_diff(ticks_ms(), timestart) >= timeout:
			print("timeout! : "+str(timeout)+" ms")
			if self.sd is not None:
				mount(self.sd, "/")
				filename = '/gps_data.txt'
				with open(filename,'a') as f:
					n = f.write("posición no determinada\n")
					f.close()
				umount("/")
			else:
				print('sd no detectada')

		self.pack = self.pos[3]+','+self.pos[4]+','+self.pos[5]+','+self.pos[6]
		# Escritura en tarjeta SD
		if self.sd is not None:
			mount(self.sd, "/")
			filename = '/gps_data.txt'
			with open(filename,'a') as f:
				n = f.write('{}\n'.format(self.pack))
				f.close()
			umount("/")
		else:
			print('sd no detectada')

	def req_pos(self):
		"""req_pos es un metodo que revisa la posicion del gps hasta que esta es correcta la funcion retorna la posicion dentro de un string"""
		self.uart.write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n') #GPRMC
		sleep(1)

		while 1:
			self.frame = self.uart.readline()
			self.pos = str(self.frame).split(',')
			try:
				if self.pos[2]=='A':
					break
			except IndexError:
				continue
			except:
				print('error desconocido')
		self.pack = self.pos[3]+','+self.pos[4]+','+self.pos[5]+','+self.pos[6]		
		return self.pack

	def req_time(self):
	# req_time es un metodo para obtener la hora de una cadena GPGGA
	# tambien transforma la hora UTC a la hora de chile la retorna en una lista
		self.uart.write(b'$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n') #GPGGA
		sleep(1)
		self.uart.readline()
		frame = self.uart.readline()
		while (frame is None or not (b'$GPGGA'==frame[0:6])) or not (b'*' in frame):
			frame = self.uart.readline()
			sleep(0.3)
		h = int(frame[7:9]) - 4
		m = int(frame[9:11])	
		s = int(frame[11:13])
		frame = self.uart.readline()
		while (frame is None or not (b'$GPRMC'==frame[0:6])) or not (b'*' in frame):
			frame = self.uart.readline()
			sleep(0.3)
		frame = str(frame)
		frame = frame.split(',')

		dia = int(frame[9][:2])
		mes = int(frame[9][2:4])
		year = int(frame[9][4:6])+2000

		print("[debug] year: {}".format(year))
		if year < 2019 or year > 2021:
			return None
		 
		"""
		dia = int(frame[57:59])
		mes = int(frame[59:61])
		year = int(frame[61:63]) + 2000
		"""
		# se le restan 4 horas al tiempo UTC
		#hora = (int(self.time[1][:2]) - 4, int(self.time[1][2:4]), int(self.time[1][4:6]))
		#return hora
		tiempo_raw = (year, mes, dia, 0 ,h, m, s, 0)
		return tiempo_raw

	def decode(self, data):
	# Metodo para decodificar las sentencias GPRMC y GPGGA
		if(data[0]=='$GPRMC'):
			self.latitud = data[3]
			self.ref_latitud = data[4]
			self.longitud = data[5]
			self.ref_longitud = data[6]
		elif(data[0]=='$GPGGA'):
			# informacion sobre la posicion
			self.latitud = data[2]
			self.ref_latitud = data[3]
			self.longitud = data[4]
			self.ref_longitud = data[5]
		else:
			pass

	# modos de arranque (time to first fix)
	def cold_start(self):
		# modo por defecto del gps
		# busca almanaque
		self.uart.write(b'$PMTK103*30\r\n')
	def full_cold_start(self):
		self.uart.write(b'$PMTK104*37\r\n')
	def warm_start(self):
		# obtiene efemerides
		self.uart.write(b'$PMTK102*31\r\n')
	def hot_start(self):
		# hot start
		self.uart.write(b'$PMTK101*32\r\n')

	# Modos de energia
	def standby_mode(self):
		self.uart.write(b'$PMTK161,0*28\r\n')
	def sleep_mode(self):
		self.uart.write(b'$PMTK161,1*29\r\n')
	def periodic_mode(self):
		# ejemplo del data
		#self.uart.write(b'$PMTK225,2,3000,12000,18000,72000*15\r\n')

		# my setup (7 segundos activo, 1 min dormido)
		#self.uart.write(b'$PMTK225,2,7000,60000,0,0*18\r\n')

		# my setup 2.0 (7 seg on 14 seg off)
		#self.uart.write(b'$PMTK225,8,7000,14000,0,0*11\r\n')

		# setup 3 (5 min on 15 min off)
		self.uart.write(b'$PMTK225,2,180000,900000,0,0*29\r\n')


	def attachSD(self, sd):
		self.sd = sd
	def nmea_out(self):
		# solo GPRMC
		self.uart.write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')
		# resetear por defecto
		#self.uart.write(b'$PMTK314,-1*04\r\n')

	# Modos sin testear
	def restore_output():
		# retorna la salida de nmea a su valor por defecto
		self.uart.write(b'PMTK314,-1*04\r\n')

	def position_fix_interval(self):
		# este parametro controla la tasa de obtencion de posicion de gps (position fix freq)
		self.uart.write(b'$PMTK500,1000,0,0,0,0*1A\r\n')

	def kill_data(self):
		self.uart.write(b'$PMTK120*31\r\n')

	def request_efemerides(self):
		# busca en las efemerides 1800 seg atras
		self.uart.write(b'$PMTK660,1800*17\r\n');
		#sleep()
		#return self.uart.read()

#		self.uart.write(b'')
