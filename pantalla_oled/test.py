from machine import I2C, Pin
import ssd1306

rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)



while 1:
	aux = mpu.read_sensors_scaled()
	x = "x: "+str(aux[0])
	y = "y: "+str(aux[1])
	z = "z: "+str(aux[2])
	oled.fill(0)
	oled.text(aux1, 0, 0)
	oled.text(aux2, 32, 0)
	oled.text(aux3, 56, 0)

	oled.show()
