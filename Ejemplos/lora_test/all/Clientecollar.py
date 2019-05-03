import ssd1306
from machine import Pin, I2C
from direccionCollar import *

def collar(lora):
    print("LoRa Receiver")
    Pin(16,Pin.OUT,value=1)
    scl=Pin(15,Pin.OUT,Pin.PULL_UP)
    sda=Pin(4,Pin.OUT,Pin.PULL_UP)
    i2c = I2C(sda=sda,scl=scl,freq=450000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.fill(0)
    display.text("Lora Receiver",0,0)
    display.show()
    while True:
        if lora.receivedPacket():
            print("Paquete recibido")
            try:
                paquete = lora.read_payload()
                direccion = paquete[0]
                print(direccion)
                print(dirCollar)
                if direccion == dirCollar:
                    comando = paquete[1]
                    mensaje = paquete[2:].decode()
                    display.fill(0)
                    display.text("Recibi esto:",0,10)
                    display.text(mensaje,0,20)
                    display.text("RSSI:{0}".format(lora.packetRssi()),0,30)
                    display.show()
                    if comando == 0:
                        paquete = bytes([0,1])+b'soy la vaca LoRa'
                        lora.bytesprintln(paquete)
                    if comando == 1:
                        paquete = bytes([0,1])+b'Hello word'
                        lora.bytesprintln(paquete)
            except Exception as e:
                print(e)