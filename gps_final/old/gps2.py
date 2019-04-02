#!/usr/bin/env python
# objeto gps del cual se puede extraer info sobre la posicion
# ademas inicializa el modulo gps
from machine import UART, Pin, I2C
from time import sleep
import ssd1306

# Pantalla
vext = Pin(21, Pin.OUT)
vext.value(0)
sleep(0.2)
rst = Pin(16, Pin.OUT)
rst.value(1)
sleep(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
Pin(21, Pin.OUT, value=1)

class Gps_upy(UART):
	def __init__(self):
		# inicializacion del modulo gps
		uart = UART(2, 115200)
		uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5) # se escogen dichos pines para no tener conflicto con oled
		#print('modulo inicializado')
	def decode_gps(self, frame):
		data = str(frame).split(',')
		if(data[0]=='$GPGSV'):
			# La cabecera es GPGSV (GPS satelites in view)
			ELEVACION = data[5]
		if(data[0]=='$GPRMC'):
			# la cabecera es GPRMC (Recommended minimum specific GPS/Transit data)
			sellodetiempo = data[1]
			if(data[2]=='A'):
				# Informacion sobre la posicion
				latitud = data[3]
				ref_latitud = data[4]
				longitud = data[5]
				ref_longitud = data[6]
				# Fecha ddmma
				dia = data[9][:2]
				mes = data[9][2:4]
				year = data[9][4:6]
				# retorno de variables
				return [latitud, ref_latitud, longitud, ref_longitud, dia, mes, year]
			else:
				print("paquete erroneo")
		if(data[0]=='$GPGGA'):
			# La cabecera es GPGGA (Global Positioning System Fix Data )
			hora = data[1][:2]
			minuto = data[1][2:4]
			segundo = data[1][4:6]
			# informacion sobre la posicion
			latitud = data[2]
			ref_latitud = data[3]
			longitud = data[4]
			ref_longitud = data[5]
			# calidad del enlace GPS
			calidad = data[6]
			return [latitud, ref_latitud, longitud, ref_longitud, hora, minuto, segundo, calidad]
		if(data[0]=='$GPGSA'):
			# La cabecera es GPGSA (GPS DOP and active satellites )
			# no contiene info relevante para el proyecto (PREGUNTAR)
			pass

gps = Gps_upy()

oled.fill(0)
oled.text('pass', 0, 0)
oled.show()



# lineas de prueba (comentar)
#gps = Gps_upy()
#sentencia_prueba = b'$GPRMC,140014.000,A,3844.7685,S,07236.9229,W,1.87,189.76,110119,,,A*60\r\n'
#gps.decode_gps(sentencia_prueba)
#print latitud