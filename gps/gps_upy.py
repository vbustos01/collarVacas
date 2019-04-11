#!/usr/bin/env python
# objeto gps del cual se puede extraer info sobre la posicion
# ademas inicializa el modulo gps
from machine import UART, Pin, I2C
from time import sleep

class Gps_upy(UART):
	def __init__(self):
		# inicializacion del modulo gps
		#uart = UART(2, 115200)
		#uart.init(115200, bits=8, parity=None, stop=1,tx=17,rx=5) # se escogen dichos pines para no tener conflicto con oled
		super(Gps_upy, self).__init__(2, 9600)
		super().init(9600, bits=8, parity=None, stop=1,tx=17,rx=5)

	def decode_gps(self):
		data = super().readline()
		data = str(frame).split(',')
		if(data[0]=='$GPRMC'):
			# la cabecera es GPRMC (Recommended minimum specific GPS/Transit data)
			sellodetiempo = data[1]
			if(data[2]=='A'):
				# Informacion sobre la posicion
				self.latitud = data[3]
				self.ref_latitud = data[4]
				self.longitud = data[5]
				self.ref_longitud = data[6]
				# Fecha ddmma
				self.dia = data[9][:2]
				self.mes = data[9][2:4]
				self.year = data[9][4:6]
			else:
				print("paquete erroneo")
		if(data[0]=='$GPGGA'):
			# informacion sobre la posicion
			self.latitud = data[2]
			self.ref_latitud = data[3]
			self.longitud = data[4]
			self.ref_longitud = data[5]

	def power_mode():
		# hot start
		#gps.write(b'$PMTK101*32\r\n')

		# warm start
		#gps.write(b'$PMTK102*31\r\n')

		# cold start
		gps.write(b'$PMTK103*30\r\n')

		# full cold start
		#gps.write(b'$PMTK104*37\r\n')

		#periodic mode
		#gps.write(b'$PMTK225,2,3000,12000,18000,72000\r\n')




# lineas de prueba (comentar)
#gps = Gps_upy()
#sentencia_prueba = b'$GPRMC,140014.000,A,3844.7685,S,07236.9229,W,1.87,189.76,110119,,,A*60\r\n'
#gps.decode_gps(sentencia_prueba)
#print latitud