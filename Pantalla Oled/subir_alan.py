from machine import I2C, Pin, ADC
from time import sleep
import ssd1306
import framebuf

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

with open('alan.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)



oled.fill(0)
oled.invert(1)
oled.blit(fbuf, 0, 0)
oled.show()


#adc = ADC(Pin(36,Pin.IN))


"""
nmuestras = 10;
i=0;
value = adc.read()
while 1:
	
	value = value + adc.read()
	sleep(0.2)
	if i==nmuestras-1:
		oled.fill(0)
		value = value/nmuestras;
		oled.text(str(value), 0, 0)
		oled.show()
		i=0
	i=i+1

	"""