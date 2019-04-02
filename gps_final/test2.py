from gps_upy2 import decode_gps
from machine import UART, Pin, I2C
from time import sleep
import ssd1306

# Pantalla
vext = Pin(21, Pin.OUT)
vext.value(0)
sleep(0.2)
rst = Pin(16, Pin.OUT)
rst.value(1)
sleep(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
Pin(21, Pin.OUT, value=1)

uart = UART(2, 115200)
gps = uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5)

frame = uart.readline()
decode_gps(frame)
# mostrar posicion por pantalla
oled.fill(0)
oled.text('longitud: {0}'.format(info_gps['longitud']), 0, 0)
oled.show()

# info es un diccionario de la forma:
#		info_gps = {
#			'latitud':None, 'ref_latitud':None,
#			'longitud':None, 'ref_longitud':None,
#		}
#while true:
#	frame = gps.readline()
#	info = gps.decode_gps(frame)
	