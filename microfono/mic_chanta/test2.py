from machine import Pin, I2C, ADC, SPI
import utime
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

# pin del led
led = Pin(25, Pin.OUT)


while 1:
	oled.fill(0)
	oled.show()
	os.mount(sd, '/fc')

	win_width = 1000
	aux = []
	muestras = 0
	tiempo_b = utime.ticks_ms()
	while muestras<win_width:
		if utime.ticks_diff(utime.ticks_ms(), tiempo_b)>=12.5:
			aux.append(adc.read())
			tiempo_b = utime.ticks_ms()
#			oled.fill(0)
#			oled.text('muestra: {}'.format(muestras), 0, 0)
#			oled.show()
			muestras = muestras + 1
	oled.text('muestras...ok', 0, 0)
	oled.show()
	filename = '/fc/audio.txt'
	for i in range(win_width):
		led.value(1)
		with open(filename,'a') as f:
			n = f.write('{},'.format(aux[i]))
		led.value(0)
	os.umount('/fc')