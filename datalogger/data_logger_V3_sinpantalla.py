"""
    Oscar Acevedo Antonio Acevedo Acevedo Antonio
    Proceso automatico para guardar informacion del modulo GPS y acelerometro en la tarjeta SD
    ademas de determinar el tiempo entre cada muestra a traves de GPS

    Nuevas caracteristicas:
        - la toma de datos debe ser a una frecuencia de 10Hz (cada 0.1 segundos), para lo cual se borran
        todas las impresiones por pantalla
"""
from machine import I2C, Pin, SPI, UART
import os
import utime
import gc
import micropython
import sdcard
import mpu6050
import ssd1306
micropython.alloc_emergency_exception_buf(100)
#####################################Inicializacion de modulos######################################
#objeto MPU
mpu = mpu6050.MPU()
# registro de sleepmode, ver anexo 4.31
#mpu.write_byte(0x6A, 0x28)
#mpu.write_byte(0x6B, 0x80)
#objeto UART/GPS
gps = UART(2, 115200)
gps.init(115200,bits=8,parity=None,stop=1,tx=17,rx=5)
#objeto SPI
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))
#objeto SD
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
###################################Control de tiempo de muestreo####################################
milis_antes = utime.ticks_ms()
intervalo = 100    # en milisegundos
# control de basura
gc.enable()

################################################loop################################################
while 1:
    milis_ahora = utime.ticks_ms()
    if(utime.ticks_diff(milis_ahora, milis_antes) >= intervalo):
        milis_antes = milis_ahora
        #se monta el sistema de archivos de la sd
        os.mount(sd, '/fc')
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
            n = f.write('{},'.format(utime.ticks_ms()))
        os.umount('/fc')
        gc.collect