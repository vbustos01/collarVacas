from machine import I2C, Pin, SPI, UART
import os
import time
import mpu6050	
import micropython
import sdcard
micropython.alloc_emergency_exception_buf(100)

#objeto MPU
mpu = mpu6050.MPU()
#objeto UART/GPS
gps = UART(2, 115200)
gps.init(9600,bits=8,parity=None,stop=1,tx=17,rx=5)
#objeto SPI
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23),miso=Pin(12),mosi=Pin(13))
#objeto SD
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))


while True:

#lectura y escritura de SD
  # Ensure right baudrate

    #se monta el sistema de archivos en la sd
    os.mount(sd, '/fc')
    print('Filesystem check')
    print(os.listdir('/fc'))
    #

    aux = gps.readline()
    gps_data = str(aux)#, "utf-8")
    filename = '/fc/gps_data.txt'

    with open(filename,'w') as f:
        n = f.write(gps_data)
        print(n, 'bytes written')


    with open(filename,'r') as f:
        result1 = f.read()
        print(len(result1), 'bytes read')

    aux = mpu.read_sensors_scaled()
    aux = aux[0] + aux[1] + aux[2]
    accelerometer_data = str(aux)
    filename = '/fc/accelerometer_data.txt'

    with open(filename,'w') as f:
        n = f.write(accelerometer_data) # one block
        print(n, 'bytes written')

    with open(filename,'r') as f:
        result2 = f.read()
        print(len(result2), 'bytes read')

    os.umount('/fc')
    time.sleep(0.8)
    Pin(25,Pin.OUT,value=0)
    time.sleep(0.8)
    Pin(25,Pin.OUT,value=1)



# print()
# print('Verifying data read back')
# success = True
# if result1 == ''.join((lines, short, lines)):
#     print('Large file Pass')
# else:
#     print('Large file Fail')
#     success = False
# if result2 == short:
#     print('Small file Pass')
# else:
#     print('Small file Fail')
#     success = False
# print()
# print('Tests', 'passed' if success else 'failed')

#sdtest.sdtest()

"""
def isr(pin):
    print("Interrupt!")
"""



#

#while True:
#	valores=mpu.read_sensors_scaled();