from gps_upy import Gps_upy
import _thread
from sd import *
from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin

# led
pinled = Pin(25, Pin.OUT)
pinvext = Pin(21, Pin.OUT)


"""
# inicializacion sd
sd = initSD()
gps = Gps_upy()

# adquisicion gps
gps.attachSD(sd)
sleep(1)
# adquisicion gps
gps.req_pos()

# adquisicion imu
imu = IMU()
imu.attachSD(sd)
imu.writesamples()

# se va a dormir 20 min
#deepsleep(1.2E6)

"""
pinled.value(1)
pinvext.value(0)
sleep(5)
deepsleep(10*1000)