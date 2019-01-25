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
    #lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
    lista = []
    val=lora.readpowertx()
    lista.append(val >> 7)
    lista.append(val >> 4 & 0x07)
    lista.append(val & 0x0f)
    lista[1]=lista[1]*.6 + 10.8
    lista[2] =lista[1] - (15 - lista[2])


    while True:
        display.fill(0)
        display.text("MODO EMISOR",0,0)
        payload = ">|{0}|HelloWOOOOOOORDDDDDLLLLLLLLLLLLLLLLL88888142".format(counter)
        #print("Sending packet: \n{}\n".format(payload))
        display.text("Envio esto:",0,10)
        display.text(payload,0,20)
        display.text("RSSI:{0}".format(lora.packetRssi()),0,30)
        display.text("{0} {1} {2}".format(lista[0],lista[1],lista[2]),0,40)
        display.text("pa  max outpwr",0,50)
        display.show()
        lora.println(payload)

        counter += 1
        sleep(0.1)