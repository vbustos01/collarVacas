from time import sleep
import ssd1306
from machine import Pin, I2C

def send(lora):
    counter = 0
    print("LoRa Sender")
    Pin(16,Pin.OUT,value=1)
    scl=Pin(15,Pin.OUT,Pin.PULL_UP)
    sda=Pin(4,Pin.OUT,Pin.PULL_UP)
    i2c = I2C(sda=sda,scl=scl,freq=450000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)

    while True:
        payload = "Hello ({0})".format(counter)
        #print("Sending packet: \n{}\n".format(payload))
        display.fill(0)
        display.text("Envio esto:",0,10)
        display.text("""{0}
                        RSSI: {1}""".format(payload, lora.packetRssi()),0,32)
        display.show()
        lora.println(payload)

        counter += 1
        sleep(0.2)

