from machine import Pin, I2C, freq
import _thread
import ssd1306
import utime
import time

# metodo para hacer parpadear el pin 25
def blinksito():
	while True:
		pin25 = Pin(25, Pin.OUT)
		utime.sleep_ms(200)
		pin25.value(1)
		utime.sleep_ms(200)
		pin25.value(0)
	

def pantalla_hellyeah():
	count = 0
	while 1:
		time.sleep(1)
		count = count + 1
		oled.fill(0)
		oled.text('holi'+str(count),5,45)
		oled.show()

def pantalla_hellyeah2():
	count = 0
	while 1:
		time.sleep(1)
		count = count + 1
		oled.fill(0)
		oled.text('holi'+str(count),5,5)
		oled.show()

# Inicializacion de la Pantalla
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
# mensaje de inicio
oled.fill(0)
oled.text('Iniciando...',0,0)
oled.show()
# modificar el registro del mpu6050 (opcional)
# 
oled.text('just blinkin\'',0,8)
oled.show()

time.sleep(1)
oled.text(str(freq()),0,32)
oled.show()
time.sleep(1)

_thread.start_new_thread(blinksito,())
time.sleep(1)
oled.text(str(freq()),0,32)
oled.show()
time.sleep(1)
_thread.start_new_thread(pantalla_hellyeah,())
time.sleep(1)
oled.text(str(freq()),0,32)
oled.show()
time.sleep(1)
_thread.start_new_thread(pantalla_hellyeah2,())
time.sleep(1)
oled.text(str(freq()),0,32)
oled.show()
time.sleep(1)
oled.text(str(freq()),0,32)
oled.show()
