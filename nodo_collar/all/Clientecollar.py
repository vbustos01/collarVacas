import ssd1306
from machine import Pin, I2C
from direccionCollar import *
from time import time
from data_frame import *

Pin(16,Pin.OUT,value=1)
#led = Pin(25,Pin.OUT,value=1)
scl = Pin(15,Pin.OUT,Pin.PULL_UP)
sda = Pin(4,Pin.OUT,Pin.PULL_UP)
i2c = I2C(sda=sda,scl=scl,freq=450000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# inicializacion de GPS:
uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1,tx=17,rx=36) # se escogen dichos pines para no tener conflicto con oled

paqueteEnviar = bytes(0)
paqueteActual = bytes(0)
intentosACK = 2
intentos = 0
paqueteSync = False
SYMB_TIME_OUT = 200


def collar(lora):
    print("LoRa Collar")
    lora.onReceive(on_receive)#Asigna una función para la interrupcion del pin DIO0
    lora.onTimeout(on_timeout,SYMB_TIME_OUT)#Asigna una función para la interrupcion del pin DIO1 y asigna un Timeout
    global display
    global paqueteActual
    global led
    sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}          
    pre_frame ={'address':255,'cmd':7,                                
                'sensors':sensors,'location':"3844.7556,S,07236.9213,W", 
                't_unix':454545666,'bateria':1024,'C_close':True}
    display.fill(0)
    display.text("LoRa Collar",0,0)
    display.show()
    lora.receive()
    paqueteActual = empaquetar(pre_frame)
    # Datos de Gps
    while True:
        try:
            posicion = uart.readline()
            if(posicion==None):
                continue
            posicion = posicion.decode("utf-8") # esto es equivalente a str() en py2
            indicador = posicion.split(',')
            if(indicador[0]=='$GPGGA'):
                posicion=posicion[18:42]
            if(indicador[0]=='$GPRMC'):
                posicion=posicion[20:44]
            pre_frame['location'] = posicion
            print(pre_frame)
        except:
            continue


def on_receive(lora,paquete):
    global intentos
    global display
    global paqueteActual
    global paqueteSync
    global paqueteEnviar
    display.fill(0)
    if paquete:
        direccion = paquete[0]
        if direccion == dirCollar:
            comando = paquete[1]
            #mensaje = paquete[2:].decode()
            display.text("Recibi:",0,10)
            if comando == 0:
                paqueteSync = True#llego un paquete de sincronización
                lora.bytesprintln(paqueteActual)
                paqueteEnviar = paqueteActual
                display.text("Sync",0,20)
                lora.receiveSingle()
            elif paqueteSync and (comando == 1):
                paqueteSync = False
                display.text("ACK",0,20)
                intentos = 0
                lora.receive()
        else:
            display.text("Direccion Diferente",0,10)
    else :
        display.text("Paquete con Error",0,10)
        lora.receive()
    if paqueteSync:
        lora.receiveSingle()
    display.text("RSSI:{0}".format(lora.packetRssi()),0,30)
    display.show()



def on_timeout(lora):
    global intentosACK
    global paqueteEnviar
    global intentos
    intentos += 1
    if intentos <= intentosACK:
        if paqueteSync:
            lora.bytesprintln(paqueteEnviar)
            lora.receiveSingle()#se espera nuevamente un ACK
    else:
        lora.receive()#intentos no cumplidos
