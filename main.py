from gps import Gps_upy
import _thread
from sd import *
from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin, ADC
import uos
#from Clientecollar import LoRa
LOW_BAT_LEVEL = 1600


pinvext = Pin(21, Pin.OUT)
pinvext.value(0)

adc = ADC(Pin(32))
adc.atten(adc.ATTN_11DB)
read = adc.read()
read = adc.read()
	
if read < LOW_BAT_LEVEL:
	deepsleep()

sd = initSD()

# Modulo GPS
gps = Gps_upy()
gps.attachSD(sd)
gps.write2sd(120000)

# Modulo IMU
imu = IMU()
imu.attachSD(sd)
imu.writesamples()

################### MODO SLEEP ##################
deepsleep(60000)