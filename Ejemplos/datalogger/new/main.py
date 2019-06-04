# ejemplo de cadena nmea
# b'$GPGSV,3,3,11,32,10,030,21,15,07,140,35,11,04,258,17*44\r\n'

oled.fill(0)
oled.text('begin', 0, 0)
oled.show()

# hot start
#gps.write(b'$PMTK101*32\r\n')

# warm start
#gps.write(b'$PMTK102*31\r\n')

# cold start
#gps.write(b'$PMTK103*30\r\n')

# full cold start
#gps.write(b'$PMTK104*37\r\n')

#periodic mode
gps.write(b'$PMTK225,2,3000,12000,18000,72000\r\n')
