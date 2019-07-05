# -*- coding: utf-8 -*-

import time
import sys
import MySQLdb
import datetime
from angles import sexa2deci
###Ejemplo diccionario obtenido al desempaquetar######################
# sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}           #
# pre_frame ={'address':255,'cmd':7,                                 #
#            'sensors':sensors,'location':[1,42,85.45,-1,72,14.25],  #
#    't_unix':4294967295,'bateria':4095,'C_close':True}              #
######################################################################
# Abre la conexion con la base de datos
#db = MySQLdb.connect('localhost','root','ufro_vacas','Vacas')

# Prepara un objeto de cursor para obtener datos usando el metodo cursor()
#cursor = db.cursor()
timeESP32 = 946684800 #tiempo de desface del RTC ESP32 (epoch of 2000-01-01 00:00:00 UTC.)
def creaTablaSiNoExiste(diccionario,db,cursor):
        # Se crean las variables y se definen los tipos
        tabla ="""CREATE TABLE IF NOT EXISTS Vaca{}(ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Fecha TEXT NOT NULL ,
        Nivel_Bateria FLOAT NOT NULL ,
        Datos_GPS BOOL,
        Datos_IMU BOOL,
        Estado_SD BOOL,
        Datos_Microfono BOOL,
        Collar_Abierto BOOL,
        Latitud FLOAT NOT NULL ,
        Longitud FLOAT NOT NULL,
        time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ) ENGINE = InnoDB;""".format(diccionario['address'])
        # Se crea la tabla
        cursor.execute(tabla)
def subirdatosVacas(diccionario):
        db = MySQLdb.connect('localhost','root','ufro_vacas','Vacas')
        cursor = db.cursor()
        creaTablaSiNoExiste(diccionario,db,cursor)
        Latitud=sexa2deci(diccionario['location'][0],diccionario['location'][1],diccionario['location'][2],0)
        Longitud=sexa2deci(diccionario['location'][3],diccionario['location'][4],diccionario['location'][5],0)
        v_s = 3.6/4096*diccionario['bateria']
        v_bat = (v_s-0.7)*16/5+0.7
        print(diccionario['t_unix'])
        date = str(datetime.datetime.utcfromtimestamp(diccionario['t_unix']+timeESP32).strftime("%Y-%m-%d %H:%M:%S"))
        tupla = (str(date),v_bat,
                (str(diccionario['sensors']['GPS'])).upper(),(str(diccionario['sensors']['IMU'])).upper(),
                (str(diccionario['sensors']['SD'])).upper(),(str(diccionario['sensors']['MIC'])).upper(),
                (str(not(diccionario['C_close']))).upper(),Latitud,Longitud) 
        # Inserta los datos a la base de datos
        cursor.execute("""INSERT INTO Vaca{} (Fecha,Nivel_Bateria,Datos_GPS,Datos_IMU,\
        Estado_SD,Datos_Microfono,Collar_Abierto,Latitud, Longitud)\
         VALUES ('%s',%f,%s,%s,%s,%s,%s,%f,%f)""".format(diccionario['address'])%tupla)
        db.commit()
        db.close()
