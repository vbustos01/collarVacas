from machine import I2C, Pin, SPI, UART
import uos
import time
import sdcard
import ssd1306

Pin(21, Pin.OUT, value=0)

# Pantalla oled
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
#i2c = I2C(scl=scl, sda=sda, freq=450000)
i2c = I2C(scl=scl, sda=sda, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.text('Iniciando', 0, 0)
oled.show()

# inicializacion modulo SD
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23), miso=Pin(14), mosi=Pin(12))


done = 0
while done < 128:
	try:
		sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
		vfs =uos.VfsFat(sd)
		uos.mount(vfs, "/")
		done = 255
	except Exception as e:
		oled.pixel(done,30,0xff)
		oled.show()
		done=done+1
		time.sleep(0.2)


gps_data = 'jaldjldjaldjklajsldkjaskj'
filename = 'gps_data.txt'
with open(filename,'w') as f:
    n = f.write(gps_data)
    print(n, 'bytes written')
with open(filename,'r') as f:
    result = f.read()
    print(len(result), 'bytes read')


if done==255:
	oled.text('Exito', 0, 20)
	oled.show()
	print("Exito")