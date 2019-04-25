from gps_upy import Gps_upy
from time import sleep
a = Gps_upy()

#a.standby_mode()
a.kill_data()
sleep(1)
# modo de inicio
a.full_cold_start()
#a.cold_start()
sleep(1)

a.nmea_out()
sleep(1)

while 1:
	a.readline()