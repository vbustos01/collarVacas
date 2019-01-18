"""
    Proceso automatico para guardar informacion del modulo GPS y acelerometro en la tarjeta SD
    las muestras se realizan cada 0.1 seg aprox
"""
from machine import I2C, Pin, SPI, UART
import os
import time
import utime
import mpu6050  
import micropython
import sdcard
import ssd1306

micropython.alloc_emergency_exception_buf(100)
#####################################Inicializacion de modulos######################################
#objeto MPU
mpu = mpu6050.MPU()
#objeto UART/GPS
gps = UART(2, 115200)
gps.init(9600,bits=8,parity=None,stop=1,tx=17,rx=5)
#objeto SPI
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))
#objeto SD
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
################################################loop################################################
while 1:
    #se monta el sistema de archivos en la sd
    os.mount(sd, '/fc')
    aux = gps.readline()
    gps_data = str(aux)
    filename = '/fc/gps_data.txt'
    with open(filename,'a') as f:
        n = f.write('{}\n'.format(gps_data))
    aux = mpu.read_sensors_scaled()
    aux = aux[0] + aux[1] + aux[2]
    accelerometer_data = str(aux)
    filename = '/fc/accelerometer_data.txt'
    with open(filename,'a') as f:
        n = f.write('{},'.format(accelerometer_data))
    filename = '/fc/time_data.txt'
    with open(filename, 'a') as f:
        #n = f.write('{},'.format(time.time()))
        n = f.write('{},'.format(utime.ticks_ms()))
    os.umount('/fc') # se desmonta la tarjeta sd