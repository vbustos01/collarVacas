from machine import UART, I2C, Pin, SPI #gps

##################inicializacion de modulos###################
# pantalla oled
try:
	scl = Pin(15, Pin.OUT, Pin.PULL_UP)
	sda = Pin(4, Pin.OUT, Pin.PULL_UP)
	i2c = I2C(scl=scl, sda=sda, freq=450000)
	oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
	# GPS
	gps = UART(2, 9600)
	gps.init(9600,bits=8,parity=None,stop=1,tx=5,rx=18)
	# acelerometro
	mpu = mpu6050.MPU()
	# tarjeta SD
	Pin(18,Pin.OUT,value=1) #para desactivar LoRa
	spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))
	sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
except:
	#mandar mensaje de error