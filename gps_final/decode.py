# Ejemplos tipicos del sensor
#eje = b'$GPGSV,3,1,10,12,67,172,16,24,58,036,18,25,50,240,,02,38,069,21*7D\r\n'
eje = b'$GPRMC,140014.000,A,3844.7685,S,07236.9229,W,1.87,189.76,110119,,,A*60\r\n'
## eje = b'$GPGGA,140030.000,3844.7430,S,07236.9182,W,1,4,3.97,124.3,M,20.8,M,,*5B\r\n'
# eje = b'$GPGSA,A,3,12,25,02,29,31,,,,,,,,2.38,2.18,0.96*00\r\n'

eje_trans = str(eje)
# arreglo con info
data = eje_trans.split(',')

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
		VELOCIDAD = data[7]
		# Fecha ddmma
		dia = data[9][:2]
		mes = data[9][2:4]
		year = data[9][4:6]
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

