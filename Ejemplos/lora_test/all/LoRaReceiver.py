import ssd1306
from machine import Pin, I2C

def receive(lora):
    print("LoRa Receiver")
    Pin(16,Pin.OUT,value=1)
    scl=Pin(15,Pin.OUT,Pin.PULL_UP)
    sda=Pin(4,Pin.OUT,Pin.PULL_UP)
    i2c = I2C(sda=sda,scl=scl,freq=450000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    contador = 0
    contadormsg = 0
    paquetesPerdidos = 0
    paquetesError = 0
    diferencia = 0
    ErroresNoDetect = 0
    while True:
        if lora.receivedPacket():
            registro = lora.getIrqFlags()

            try:
                payload = lora.read_payload()
                display.fill(0)
                display.text("Recibi esto:",0,10)
                str1 = payload.decode()
                str2 = str1.split('|')[2] 
                display.text(str1,0,20)
                display.text("RSSI:{0}".format(lora.packetRssi()),0,30)
                if contador == 99:
                    contador = 0
                    paquetesPerdidos = 0
                    paquetesError = 0
                    ErroresNoDetect = 0
                if contador > 0: 
                    diferencia =int(str1.split('|')[1]) - contadormsg
                if diferencia >= 2:
                    paquetesPerdidos+=diferencia-1
                
                if (registro & 0x20) == 1:
                    paquetesError += 1
                if str2 != 'HelloWOOOOOOORDDDDDLLLLLLLLLLLLLLLLL88888142':
                    ErroresNoDetect += 1

                display.text("Perdida: {0}%".format(paquetesPerdidos),0,40)
                display.text("E:{0} E.N.D:{1}".format(paquetesError,ErroresNoDetect),0,50)
                contador += 1
                display.show()
                #print("*** Received message ***\n{}".format(payload.decode()))
                contadormsg = int(str1.split('|')[1])
            except Exception as e:
                print(e)
            #display.show_text("RSSI: {}\n".format(lora.packetRssi()), 10, 10)
            #print("with RSSI: {}\n".format(lora.packetRssi))