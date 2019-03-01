from machine import UART
gps = UART(2, 9600)
gps.init(9600,bits=8,parity=None,stop=1,tx=5,rx=18)

gps.write(b'$PMTK225, 0*0B<CR><LF>')
gps.write(b'$PMTK223,1,25,180000,60000*38<CR><LF>')
gps.write(b'$PMTK225,1,3000,12000,18000,72000*16<CR><LF>')