from machine import Pin, SPI
from drivers import sdcard

def initSD():
	counter = 0
	vext_pin = Pin(21, Pin.OUT, value = 0)
	cs_lora = Pin(18,Pin.OUT,value=1) #para desactivar LoRa
	while counter < 3:
		spi = SPI(sck=Pin(23), mosi=Pin(27), miso=Pin(19))
		try:
			sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
			return sd
		except Exception as e:
			print("Error al montar sd, intento "+str(counter))
			spi.deinit()
		counter += 1
	return None