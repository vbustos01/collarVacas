from machine import I2C, Pin, UART
from time import sleep
import ssd1306

# Pantalla
vext = Pin(21, Pin.OUT)
vext.value(0)
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
Pin(21, Pin.OUT, value=1)

# inicializacion de GPS:
uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5) # se escogen dichos pines para no tener conflicto con oled

# trucazo:
rst = Pin(16, Pin.OUT)
rst.value(1)


# adquisicion (esto debe realizarse cada 15 min):
while 1:
	posicion = uart.readline()
	if(posicion==None):
		continue
	posicion = posicion.decode("utf-8") # esto es equivalente a str() en py2
	posicion = posicion.split(',')
	if((posicion[0]=='$GPGGA')|(posicion[0]=='$GPRMC')):
		break

# uso de pantalla
oled.fill(0)
oled.text(posicion[2], 0, 0)
oled.show()

