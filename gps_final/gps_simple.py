from gps_upy2 import decode_gps

test = b'$GPRMC,171930.000,A,3844.7576,S,07236.9225,W,0.41,183.71,160119,,,A*6F\r\n'
info = decode_gps(test)
print(info)