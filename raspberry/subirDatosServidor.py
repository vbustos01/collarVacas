# -*- coding: utf-8 -*-

import time
import sys
import pymysql
import datetime
from angles import sexa2deci
###Ejemplo diccionario obtenido al desempaquetar######################
# sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}           #
# pre_frame ={'address':255,'cmd':7,                                 #
#            'sensors':sensors,'location':[1,42,85.45,-1,72,14.25],  #
#    't_unix':4294967295,'bateria':4095,'C_close':True}              #
######################################################################
# Abre la conexion con la base de datos
db = pymysql.connect('localhost','root','ufro_vacas','Vacas')

# Prepara un objeto de cursor para obtener datos usando el metodo cursor()
cursor = db.cursor()

def creaTablaSiNoExiste(diccionario):
        global cursor
        global db
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
         `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ) ENGINE = InnoDB;""".format(diccionario['address'])

        # Se crea la tabla
        cursor.execute(tabla)
def subirdatosVacas(diccionario):
        creaTablaSiNoExiste(diccionario)
        global cursor
        global db
        Latitud=sexa2deci(diccionario['location'][0],diccionario['location'][1],diccionario['location'][2],0)
        Longitud=sexa2deci(diccionario['location'][3],diccionario['location'][4],diccionario['location'][5],0)
        tupla = (diccionario['address'],diccionario['t_unix'],diccionario['bateria'],
                diccionario['sensors']['GPS'],diccionario['sensors']['IMU'],
                diccionario['sensors']['SD'],diccionario['sensors']['MIC'],not diccionario['C_close'],
                Latitud,Longitud) 
        # Inserta los datos a la base de datos
        cursor.execute("INSERT INTO Vaca{0} (ID,Fecha,Nivel_Bateria,Datos_GPS,Datos_IMU,Estado_SD,Datos_Microfono,Collar_Abierto,Latitud, Longitud) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%f,%f)".format(diccionario['address']),tupla)
        db.commit()
        db.close()


