#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
import MySQLdb
import datetime

# Credenciales servidor
host = "localhost"
usuario = "phpmyadmin"
clave = "66662841"
base_de_datos = "Vacas"

# Abre la conexion con la base de datos
db = MySQLdb.connect(host, usuario, clave, base_de_datos)

# Prepara un objeto de cursor para obtener datos usando el metodo cursor()
cursor = db.cursor()

diccionario = {'ID': 1, 'Fecha': 'algo',
'Nivel_bateria': 'algo', 'Datos Gps': 'algo',
'Datos IMU': 'algo', 'Estado SD': 'algo',
'Datos Microfono': 'algo', 'Latitud': 'algo',
'Longitud': 'algo'}

def creaTablaSiNoExiste():

        # Se crean las variables y se definen los tipos
        tabla = """CREATE TABLE IF NOT EXISTS Vaca{0} ( `ID` INT NOT NULL ,
         `Fecha` TEXT NOT NULL ,
         `Nivel_Bateria` FLOAT NOT NULL ,
         `Datos_GPS` BOOLEAN NOT NULL ,
         `Datos_IMU` BOOLEAN NOT NULL ,
         `Estado_SD` BOOLEAN NOT NULL ,
         `Datos_Microfono` BOOLEAN NOT NULL ,
         `Collar_Abierto` BOOLEAN NOT NULL ,
         `Latitud` FLOAT NOT NULL ,
         `Longitud` FLOAT NOT NULL,
         `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ) ENGINE = InnoDB;""".format(diccionario['ID'])

        # Se crea la tabla
        cursor.execute(tabla)
def subirdatosVacas():

        # Configuracion del tipo de sensor DHT
        sensor = Adafruit_DHT.DHT11

        # Configuracion del puerto GPIO al cual esta conectado  (GPIO 23)
        pin = 23

        # Lee los datos de temperatura y humedad del DHT11 y los almacena
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Imprime los datos de temperatura y humedad
        if humidity is not None and temperature is not None:
                print('Temperature={0:0.1f}°C Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
                print('Failed to get reading. Try again!')
                sys.exit(1)

        unix = int(time.time())
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

        # Inserta los datos a la base de datos
        cursor.execute("INSERT INTO Vaca{0} (ID, Latitud, Longitud) VALUES (%s, %s, %s)".format(diccionario['ID']),(diccionario['ID'], temperature, humidity))
        db.commit()

creaTablaSiNoExiste()

# Sube datos infinitamente
while True:

        subirdatosVacas()
        time.sleep(10)

db.close()

