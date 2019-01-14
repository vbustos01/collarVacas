from machine import I2C, Pin, SPI, UART
import os
import time
import sdcard
import ssd1306

# Pantalla oled
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oled.fill(0)
oled.text('Iniciando', 0, 0)
oled.show()

# inicializacion modulo SD
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23), miso=Pin(12), mosi=Pin(13))
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))

oled.fill(0)
oled.text('Modulo listo', 0, 0)
oled.show()


os.mount(sd, '/fc')
gps_data = 'hola secsua'
filename = '/fc/gps_data.txt'


with open(filename,'w') as f:
    n = f.write(gps_data)
    print(n, 'bytes written')
with open(filename,'r') as f:
    result1 = f.read()
    print(len(result1), 'bytes read')

os.umount('/fc')
time.sleep(0.8)
Pin(25,Pin.OUT,value=0)
time.sleep(0.8)
Pin(25,Pin.OUT,value=1)
