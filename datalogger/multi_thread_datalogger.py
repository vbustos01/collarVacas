from machine import Pin, I2C
import _thread
import ssd1306
import utime

# metodo para hacer parpadear el pin 25
def blinksito():
	while 1:
		pin25 = Pin(25, Pin.OUT)
		utime.sleep_ms(200)
		pin25.value(1)
		utime.sleep_ms(200)
		pin25.value(0)

def pantalla_hellyeah():
	while 1:
		oled.fill(0)
		oled.text('holi',5,45)
		oled.show()

# Inicializacion de la Pantalla
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
# mensaje de inicio
oled.fill(0)
oled.text('Iniciando...',0,0)
oled.show()
# modificar el registro del mpu6050 (opcional)
# 
oled.text('just blinkin\'',0,8)
oled.show()
_thread.start_new_thread(blinksito())

oled.text('blinkeando\'',0,16)
oled.show()
