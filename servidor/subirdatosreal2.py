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
base_de_datos = "DHT11"

# Abre la conexion con la base de datos
db = MySQLdb.connect(host, usuario, clave, base_de_datos)

# Prepara un objeto de cursor para obtener datos usando el metodo cursor()
cursor = db.cursor()

# Se crea una tabla y sus variables (Si la tabla con ese nombre ya existe, no se crea,
# pero se actualiza)
cursor.execute("DROP TABLE IF EXISTS datosreal")

tabla = """CREATE TABLE datosreal ( `ID` INT NOT NULL AUTO_INCREMENT ,
`Tiempo` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , 
`Temperatura` INT NOT NULL , 
`Humedad` INT NOT NULL , PRIMARY KEY (`ID`)) ENGINE = InnoDB;"""

cursor.execute(tabla)

def subirdatos_DHT11():
     """
     sensor_args = { '11': Adafruit_DHT.DHT11,
                                '22': Adafruit_DHT.DHT22,
                                '2302': Adafruit_DHT.AM2302 }
     if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
                                sensor = sensor_args[sys.argv[1]]
                                pin = sys.argv[2]
     else:
                                print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
                                print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
                                sys.exit(1)
     """

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
     cursor.execute("INSERT INTO datosreal (Temperatura, Humedad) VALUES (%s, %s)",(temperature, humidity))

     db.commit()

# Sube datos infinitamente
while True:
     subirdatos_DHT11()
     time.sleep(10)
db.close()
