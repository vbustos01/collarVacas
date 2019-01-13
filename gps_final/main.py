import gps_decoder

if __name__ == '__main__':
	hola = b'$GPGSV,3,1,10,12,67,172,16,24,58,036,18,25,50,240,,02,38,069,21*7D\r\n'
	print gps_decoder.decode_gps(hola)