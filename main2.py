from gps import Gps_upy
import _thread
from sd import *
#from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin
import uos
from Clientecollar import LoRa


"""
# LoRa
l = LoRa()
l.beginIRQ()

sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}          
pre_frame ={'address':255,'cmd':7,                                
	'sensors':sensors,'location':"3844.7556,S,07236.9213,W", 
	't_unix':123456123,'bateria':1024,'C_close':True}
l.setMsn(pre_frame)

"""
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

# Modulo GPS
gps = Gps_upy()
gps.attachSD(sd)
gps.write2sd()

# Modulo IMU
imu = IMU()
imu.attachSD(sd)
imu.writesamples()

################### MODO SLEEP ##################
deepsleep(1.2E6)

