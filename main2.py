# Main creado con la intencion de tomar muestras de imu
from gps import GPS
import _thread
from sd import *
from imu import *
from time import sleep, ticks_ms
from machine import Timer, deepsleep, Pin, RTC, ADC
import uos
from drivers.direccionCollar import *
from lora import *
import utime
################# Sensado de bateria
LOW_BAT_LEVEL = 1600
pinvext = Pin(21, Pin.OUT)
pinvext.value(0)
adc = ADC(Pin(32))
adc.atten(adc.ATTN_11DB)
adc.read() # se consume la primera lectura, ya que da una medicion erronea 
# promedio de muestras de adc
###################

	# Modulo SD
sd = initSD()
	# Modulo GPS
gps = GPS()
gps.attachSD(sd)
#gps.write2sd()
gps_time = gps.req_time()
	# Seteo de la hora 
rtc = RTC()
rtc.datetime(gps_time)

	# Modulo IMU
imu = IMU()
imu.attachSD(sd)
# interrupcion
imu.irq_enable()
imu.setsamplerate(10)
imu.fifo_enable()
def foo():
	aux = imu.dumpfifo()
	aux = imu.sortfifo(aux)
	print(ticks_ms())

	if sd is not None:
		uos.mount(sd,'/')
		lista_dir = uos.listdir()
		count = 0
		while ('acc%d.csv' % (count)) in lista_dir:
			count = count + 1
		print(count)
		f = open('acc%d.csv' % (count), 'a')
		f.write("{},{}\n".format(imu.readtostring(aux[0]),rtc.datetime()))
		for i in aux[1:len(aux)]:
			f.write("{}\n".format(imu.readtostring(i)))
		f.close()
		uos.umount("/")

# pin de interrupcion
fof = Pin(36, Pin.IN, Pin.PULL_UP)
fof.irq(lambda x: foo(), Pin.IRQ_RISING)

while 1:
	promedio = 0
	for i in range(100):
		promedio = promedio + adc.read()
	promedio = promedio / 100
	# respaldo promedio
	if promedio < LOW_BAT_LEVEL:
		deepsleep()

	t_aux = utime.mktime(rtc.datetime()[0:3] + rtc.datetime()[4:7] + (0,0))

	posicion = gps.req_pos()
	sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False} 
	pre_frame ={'address':dirCollar,'cmd':7,                                
		'sensors':sensors,'location':posicion, 
		't_unix':4294967295,'bateria':int(promedio),'C_close':True}
	lora_th.addMsn2cola(pre_frame)
	sleep(5)
