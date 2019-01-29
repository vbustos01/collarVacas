from machine import Pin, ADC
from time import sleep


pinADC = Pin(36)
pinled = Pin(25, Pin.OUT)
adc = ADC(pinADC)
adc.atten(adc.ATTN_11DB)
#apin = adc.channel(pin='GP26')
periodoms = 1000
estadoled = 0

while True:
	periodoms = adc.read()
	pinled.value(estadoled)
	sleep(periodoms/1000)
	if estadoled==0:
		estadoled=1
	else:
		estadoled=0