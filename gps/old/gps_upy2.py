def decode_gps(frame):
	data = str(frame).split(',')
	info_gps = {'latitud':None, 'ref_latitud':None,'longitud':None, 'ref_longitud':None}
	# Discriminacion de sentencias NMEA segun su cabecera
	if(data[0]=='$GPRMC'):
		info_gps['latitud'] = data[3]
		info_gps['ref_latitud'] = data[4]
		info_gps['longitud'] = data[5]
		info_gps['ref_longitud'] = data[6]
	if(data[0]=='$GPGGA'):
		info_gps['latitud'] = data[2]
		info_gps['ref_latitud'] = data[3]
		info_gps['longitud'] = data[4]
		info_gps['ref_longitud'] = data[5]
	return info_gps

#test = b'$GPRMC,171930.000,A,3844.7576,S,07236.9225,W,0.41,183.71,160119,,,A*6F\r\n'
#info = {}
#info = decode_gps(test)
#print(info)