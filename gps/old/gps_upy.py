#!/usr/bin/env python
from time import sleep
import ssd1306


class Gps_upy():
	def __init__(self):
#		print 'Modulo gps inicializado'

		pass
	def decode_gps(self, frame):
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
	def start_mode()


# pruebas objeto
#test = b'$GPRMC,171930.000,A,3844.7576,S,07236.9225,W,0.41,183.71,160119,,,A*6F\r\n'
#gps = Gps_upy()
#info = gps.decode_gps(test)
#print info['longitud']
