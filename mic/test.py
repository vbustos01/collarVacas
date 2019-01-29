from machine import Pin, I2C, ADC, SPI
import ssd1306
import sdcard
import micropython
import os

micropython.alloc_emergency_exception_buf(100)

#inicializacion de pantalla
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

#inicializacion ADC
pinADC = Pin(36)
adc = ADC(pinADC)
adc.atten(adc.ATTN_11DB)
oled.text('ADC...OK ', 0, 8)
oled.show()

#configuracion SD
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
oled.text('SD...OK', 0, 16)
oled.show()

while 1:
	oled.fill(0)
	os.mount(sd, '/fc')
	aux = str(adc.read())
	filename = '/fc/audio.txt'
	with open(filename,'a') as f:
		n = f.write('{},'.format(aux))
	os.umount('/fc')