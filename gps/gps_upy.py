#!/usr/bin/env python
# objeto gps del cual se puede extraer info sobre la posicion
# ademas inicializa el modulo gps
from machine import UART, Pin, I2C
from time import sleep

class Gps_upy(UART):
	def __init__(self):
		super(Gps_upy, self).__init__(2, 9600)
		super().init(9600, bits=8, parity=None, stop=2,tx=17,rx=5)
		# configurar gps a 9600 baud
		#super().write(b'$PMTK251,9600*27\r\n')

	def leer_parasiempre(self):
		for i in range(1,12):
			print(super().read())
			sleep(2)

	# Metodo para decodificar las sentencias
	def decode_gps(self):
		data = super().readline()
		data = str(frame).split(',')
		if(data[0]=='$GPRMC'):
			self.latitud = data[3]
			self.ref_latitud = data[4]
			self.longitud = data[5]
			self.ref_longitud = data[6]
		if(data[0]=='$GPGGA'):
			# informacion sobre la posicion
			self.latitud = data[2]
			self.ref_latitud = data[3]
			self.longitud = data[4]
			self.ref_longitud = data[5]

	# modos de arranque (time to first fix)
	def cold_start(self):
		# modo por defecto del gps
		# busca almanaque
		super().write(b'$PMTK103*30\r\n')
	def full_cold_start(self):
		super().write(b'$PMTK104*37\r\n')
	def warm_start(self):
		# obtiene efemerides
		super().write(b'$PMTK102*31\r\n')
	def hot_start(self):
		# hot start
		super().write(b'$PMTK101*32\r\n')

	# Modos sin testear
	def periodic_mode(self):
		#periodic mode
		super().write(b'$PMTK225,2,3000,12000,18000,72000\r\n')

	def nmea_out(self):
		# configuracion de la frecuencia de salida de las sentencias
		super().write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')
		# resetear por defecto
		#super().write(b'$PMTK314,-1*04\r\n')

	def sleep_mode(self):
		# Sleep mode: In this mode the receiver stays at full on power state. This mode can be waken up by the host
		# sending the command through the communication interface or external interrupt.
		pass

	def position_fix_interval(self):
		# este parametro controla la tasa de obtencion de posicion de gps (position fix freq)
		super().write(b'$PMTK500,1000,0,0,0,0*1A\r\n')
	def request_efemerides(self):
		# busca en las efemerides 1800 seg atras
		super().write(b'$PMTK660,1800*17\r\n');
		#sleep()
		#return super().read()

#		super().write(b'')
