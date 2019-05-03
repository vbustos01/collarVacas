from gps_upy import Gps_upy
import _thread
from sd import *
#from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin
import uos
from Clientecollar import LoRa




# led
#pinled = Pin(25, Pin.OUT)
#pinvext = Pin(21, Pin.OUT)
#pinled.value(1)


# LoRa
l = LoRa()
l.beginIRQ()

sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}          
pre_frame ={'address':255,'cmd':7,                                
	'sensors':sensors,'location':"3844.7556,S,07236.9213,W", 
	't_unix':454545666,'bateria':1024,'C_close':True}
l.setMsn(pre_frame)





# Modulo SD
sd = initSD()
if sd==None:
	print("tamalo")
else:
	uos.mount(sd, '/')
	f = open('hol123.txt', 'w')
	f.write('holiiiiiiiiiii')
	f.close()
	uos.umount('/')
"""
# Modulo GPS
gps = Gps_upy()
gps.attachSD(sd)
gps.req_pos()

# Modulo IMU
imu = IMU()
imu.attachSD(sd)
imu.writesamples()

# se va a dormir 20 min
deepsleep(1.2E6)

#deepsleep(10*1000)

"""