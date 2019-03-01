from machine import I2C, Pin, SPI, UART
import os
import time
import mpu6050	
import micropython
import sdcard
import ssd1306

micropython.alloc_emergency_exception_buf(100)

# Pantalla oled
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.text('Iniciando', 0, 0)
oled.show()

#objeto MPU
mpu = mpu6050.MPU()


#objeto UART/GPS
gps = UART(2, 115200)
gps.init(9600,bits=8,parity=None,stop=1,tx=17,rx=5)
oled.text('Gps...OK', 0, 10)
oled.show()
#objeto SPI
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
#spi = SPI(sck=Pin(23),miso=Pin(12),mosi=Pin(13))
# trucazo (el pin 12 da problemas)
spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))

#objeto SD
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
oled.text('SD...OK', 0, 20)
oled.show()

# contador auxiliar para controlar numero de ciclos
cont = 1

while True:
    #lectura y escritura de SD
    # Ensure right baudrate
    #se monta el sistema de archivos en la sd
    os.mount(sd, '/fc')
    print('Filesystem check')
    print(os.listdir('/fc'))
    aux = gps.readline()
    gps_data = str(aux)#, "utf-8")
    filename = '/fc/gps_data.txt'
    
    oled.text('Escribiendo SD', 0, 30)
    oled.show()
    
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

    #reseteo pantalla
    oled.fill(0)

    #contador
    cont = cont + 1
    if cont > 5:
        oled.text('Escribiendo SD', 0, 30)
        oled.show()
        break

# Proceso terminado
oled.fill(0)
oled.text('Fin, Todo OK', 5, 45)
oled.show()

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

