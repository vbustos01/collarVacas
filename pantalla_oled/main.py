from machine import I2C, Pin, ADC
from time import sleep
import ssd1306

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

adc = ADC(Pin(36,Pin.IN))
adc.atten(ADC.ATTN_6DB)

nmuestras = 10;
i=0;

while 1:
	value = adc.read()
	"""
	for x in range(1,nmuestras):
		value = value + adc.read()
	value = value/10
	"""
	oled.fill(value);
	oled.show()
	"""
	oled.text(str(value),32,32)
	oled.text(str(3*value/4096),32,16)
	oled.show()
	"""
	sleep(0.1)