from machine import Pin, I2C
from drivers import mpu6050
from drivers import ssd1306
import time

rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

mpu = mpu6050.MPU()


while 1:
	aux = mpu.read_sensors_scaled()
	x = "x: "+str(aux[0])
	y = "y: "+str(aux[1])
	z = "z: "+str(aux[2])
	oled.fill(0)
	oled.text(x, 0, 0)
	oled.text(y, 0, 8)
	oled.text(z, 0, 16)
	oled.show()
	time.sleep(0.2)