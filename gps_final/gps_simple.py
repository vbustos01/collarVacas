import ssd1306
from machine import Pin, I2C, UART
from time import time,sleep


vext = Pin(21, Pin.OUT)
vext.value(0)
sleep(0.2)
rst = Pin(16, Pin.OUT)
rst.value(1)
sleep(1)
Pin(16,Pin.OUT,value=1)
#led = Pin(25,Pin.OUT,value=1)
scl = Pin(15,Pin.OUT,Pin.PULL_UP)
sda = Pin(4,Pin.OUT,Pin.PULL_UP)
i2c = I2C(sda=sda,scl=scl,freq=450000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# inicializacion de GPS:
uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5) # se escogen dichos pines para no tener conflicto con oled

#test = b'$GPRMC,171930.000,A,3844.7576,S,07236.9225,W,0.41,183.71,160119,,,A*6F\r\n'
#test = test.decode("utf-8") 

# Datos de Gps
while True:
    posicion = uart.readline()
    if(posicion==None):
        continue
    posicion = posicion.decode("utf-8") # esto es equivalente a str() en py2
    indicador = posicion.split(',')
    if(indicador[0]=='$GPGGA'):
        posicion=posicion[18:42]
        break
    if(indicador[0]=='$GPRMC'):
        posicion=posicion[20:44]
        break

display.fill(0)
display.text(posicion, 0, 0)
display.show()