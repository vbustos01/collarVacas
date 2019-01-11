from machine import I2C, Pin, UART
import ssd1306

# el pin de reset debe estar en HIGH (se resetea en LOW)
rst = Pin(16, Pin.OUT)
rst.value(1)
# inicializacion de la pantalla oled
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
# inicializacion de GPS
uart = UART(2, 115200)
uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=5) # se escogen dichos pines para no tener conflicto con oled
# uso de pantalla
oled.fill(0)
oled.text('pop', 0, 0)
oled.show()

