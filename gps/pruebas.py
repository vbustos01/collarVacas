# inicializacion gps
from gps_upy import Gps_upy
from time import sleep
import utime
a = Gps_upy()

####################### comienzo pruebas #####################

# limpieza
a.kill_data()
print('info borrada')
sleep(1)
a.nmea_out()
sleep(2)
a.read()
a.read()

##################### FULL COLD START #################
t_init = utime.ticks_ms()
a.full_cold_start()
sleep(1)

while 1:
	try:
		a.readline()
	except KeyboardInterrupt:
		break
	except:
		print('error desconocido.')
t_fcold = utime.ticks_diff(utime.ticks_ms(), t_init)
print('tiempo guardado')
# limpieza 2
a.kill_data()
print('info borrada')
sleep(1)
a.nmea_out()
sleep(2)
a.read()
a.read()

##################### COLD START ###################
oled.fill(0)
oled.text('Cold start', 0, 0)
t_init = utime.ticks_ms()
a.cold_start()
sleep(1)

while 1:
	try:
		a.readline()
	except KeyboardInterrupt:
		break
	except:
		print('error desconocido.')
t_cold = utime.ticks_diff(utime.ticks_ms(), t_init)


# limpieza 3
a.kill_data()
print('info borrada')
sleep(1)
a.nmea_out()
sleep(2)
a.read()
a.read()

##################### WARM START ###################
oled.fill(0)
oled.text('Warm start', 0, 0)
t_init = utime.ticks_ms()
a.warm_start()
sleep(1)

while 1:
	try:
		a.readline()
	except KeyboardInterrupt:
		break
	except:
		print('error desconocido.')
t_warm = utime.ticks_diff(utime.ticks_ms(), t_init)

# limpieza 4
a.kill_data()
print('info borrada')
sleep(1)
a.nmea_out()
sleep(2)
a.read()
a.read()

##################### HOT START ###################
t_init = utime.ticks_ms()
a.hot_start()
sleep(1)

while 1:
	try:
		a.readline()
	except KeyboardInterrupt:
		break
	except:
		print('error desconocido.')
t_hot = utime.ticks_diff(utime.ticks_ms(), t_init)

################# RESULTADOS ######################
print('Tiempos: ')
print('full cold start :{}'.format(t_fcold))
print('cold start :{}'.format(t_cold))
print('warm start :{}'.format(t_warm))
print('hot start :{}'.format(t_hot))
