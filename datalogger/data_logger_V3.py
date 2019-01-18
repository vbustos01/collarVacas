"""
    Proceso automatico para guardar informacion del modulo GPS y acelerometro en la tarjeta SD
    ademas de determinar el tiempo entre cada muestra a traves de GPS

    Nuevas caracteristicas:
        - la toma de datos debe ser a una frecuencia de 10Hz (cada 0.1 segundos), para lo cual se borran
        todas las impresiones por pantalla
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
# Pantalla oled
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.text('Iniciando (t={})'.format(utime.ticks_ms()), 0, 0)
oled.show()
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
###################################Control de tiempo de muestreo####################################
milis_antes = utime.ticks_ms()
intervalo = 100    # en milisegundos
oled.text('(t={})'.format(utime.ticks_ms()), 0, 8)
oled.show()
################################################loop################################################
while 1:
    milis_ahora = utime.ticks_ms()
    if(utime.ticks_diff(milis_ahora, milis_antes) >= intervalo):
        milis_antes = milis_ahora
        #se monta el sistema de archivos en la sd
        os.mount(sd, '/fc')
        # INFORMACION MODULO GPS
        aux = gps.readline()
        gps_data = str(aux)
        filename = '/fc/gps_data.txt'
        with open(filename,'a') as f:
            n = f.write('{}\n'.format(gps_data))
        # INFORMACION MODULO ACELEROMETRO
        aux = mpu.read_sensors_scaled()
        aux = aux[0] + aux[1] + aux[2]
        accelerometer_data = str(aux)
        filename = '/fc/accelerometer_data.txt'
        # el parametro 'a' deriva de 'append' (adjuntar)
        with open(filename,'a') as f:
            n = f.write('{},'.format(accelerometer_data))
        # escribe informacion sobre el tiempo
        filename = '/fc/time_data.txt'
        with open(filename, 'a') as f:
            n = f.write('{},'.format(time.time()))
        os.umount('/fc')