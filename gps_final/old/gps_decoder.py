#!/usr/bin/env python
""" Metodo para decodificar cadenas NMEA """

def decode_gps(frame):
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
	if(data[0]=='$GPGSA'):
		# La cabecera es GPGSA (GPS DOP and active satellites )
		# no contiene info relevante para el proyecto (PREGUNTAR)
		pass