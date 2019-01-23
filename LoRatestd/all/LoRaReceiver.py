import ssd1306
from machine import Pin, I2C

def receive(lora):
    Pin(16,Pin.OUT,value=1)
    scl=Pin(15,Pin.OUT,Pin.PULL_UP)
    sda=Pin(4,Pin.OUT,Pin.PULL_UP)
    i2c = I2C(sda=sda,scl=scl,freq=450000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.text("Lora Receiver",0,10)

    while True:
        if lora.receivedPacket():
            lora.blink_led()

            try:
                payload = lora.read_payload()
                display.fill(0)
                display.text("Recibi esto:",0,10)
                display.text("{0} RSSI: {1}".format(payload.decode(), lora.packetRssi()),0,32)
                display.show()
                #print("*** Received message ***\n{}".format(payload.decode()))

            except Exception as e:
                print(e)
                display.text("Exception:",0,10)
            #display.show_text("RSSI: {}\n".format(lora.packetRssi()), 10, 10)
            #print("with RSSI: {}\n".format(lora.packetRssi))

