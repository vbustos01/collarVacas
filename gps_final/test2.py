from machine import UART, Pin, I2C
from time import sleep
import ssd1306

# funcion que decodifica las tramas
def decode_gps(frame):
	######################################################
	# ESTA FUNCION RETORNA UN DICCIONARIO CON INFO SOBRE:
	# - latitud
	# - longitud
	######################################################		
	# la sentencia NMEA se separa por sus comas:
	data = str(frame).split(',')
	# frame que contendra la info decodificada:
	info_gps = {
		'latitud':None, 'ref_latitud':None,
		'longitud':None, 'ref_longitud':None,
	}

	# Discriminacion de sentencias NMEA segun su cabecera
	if(data[0]=='$GPGSV'):
		ELEVACION = data[5]
	if(data[0]=='$GPRMC'):
		sellodetiempo = data[1]
		if(data[2]=='A'):
			# Informacion sobre la posicion
			info_gps['latitud'] = data[3]
			info_gps['ref_latitud'] = data[4]
			info_gps['longitud'] = data[5]
			info_gps['ref_longitud'] = data[6]

			# Fecha ddmma (por el momento no)
			#dia = data[9][:2]
			#mes = data[9][2:4]
			#year = data[9][4:6]
			return info_gps
		else:
			print("paquete erroneo")
	if(data[0]=='$GPGGA'):
		# informacion sobre la hora (por el momento no)
		#hora = data[1][:2]
		#minuto = data[1][2:4]
		#segundo = data[1][4:6]
		
		# informacion sobre la posicion
		info_gps['latitud'] = data[2]
		info_gps['ref_latitud'] = data[3]
		info_gps['longitud'] = data[4]
		info_gps['ref_longitud'] = data[5]
		# calidad del enlace GPS
		calidad = data[6]

		return info_gps
	if(data[0]=='$GPGSA'):
		# La cabecera es GPGSA (GPS DOP and active satellites )
		# no contiene info relevante para el proyecto (PREGUNTAR)
		pass

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

uart = UART(2, 115200)
uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5)

# lectura del sensor
frame = uart.readline()

# mostrar posicion por pantalla
oled.fill(0)
oled.text('longitud: {0}'.format(info_gps['longitud']), 0, 0)
oled.show()

# info es un diccionario de la forma:
#		info_gps = {
#			'latitud':None, 'ref_latitud':None,
#			'longitud':None, 'ref_longitud':None,
#		}
