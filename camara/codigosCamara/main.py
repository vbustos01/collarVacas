	# -*- coding: utf-8 -*-

from ptz_cam import ptzcam
from time import sleep
from funciones_cam import seguimiento,getData,controlZoom,controlTilt
from interpolacion import interpolTilt,interpolZoom,interpolPan
from pan import controlPan
from pruebagps import revision
""" 
INFORMACION DE CODIGO

caracteristicas codigo:
	*algoritmo de seguimiento de collar.
	*cuenta de 3 archivos .py base:
		*ptz_cam: donde se fijan comandos de la camara,se inicializa y configura esta misma, por protocolo ONVIF.
		*funciones_cam: donde se definen las funciones a utilizar en el codigo principal (conversion coordenadas gps-coordenadas camara).
		*main: codigo principal cuyos trabajos son:
			-inicializar camara.
			-obtener posicion actual camara.
			-obtencion de coordenadas gps.
			-calculo de posicion requerida por gps.
			-movimiento camara.
			*todo dentro de un ciclo infinito*
caracteristicas camara:

*camara ptz que puede girar sobre su eje sin un tope en el giro.
*dos de las coordenadas de la camara (pan,tilt) son una especie de coordenadas esfericas que van entre -1 y 1, pasando por cero
	mientras que la coordenada restante (zoom) va desde 0 a 1
* las ips de las camaras son: 192.168.1.108 y 192.168.1.109 , y tienen mismo usuario y contraseña.
		tareas que restan:
			*control del limpiador de lente. 
			*poder extraer coordenadas gps desde el servidor
			*revisar el correcto funcionamiento de las funciones seguimiento,controlTiltZoom 

*********************************************
fecha de actualizacion comentarios: 13/07/19
*********************************************
"""
ip1='172.22.120.193' #camara sur
ip2='172.22.120.194' #camara norte


#se crea el objeto ptz
vaca1=ptzcam(ip1)

if True:
	#sleep(12)
	#extrar posicion actual de la camara
	x=vaca1.status.Position.PanTilt._x # pan - eje horizontal
	y=vaca1.status.Position.PanTilt._y #tilt - eje vertical
	z=vaca1.status.Position.Zoom._x # zoom


	print 'posicion actual camara:', x,y,z
	# observacion! se dejo las variables como x,y,z por comodidad, pudiendo ser remplazadas en un futuro 


	#posicion requerida a apuntar
	print 'tomando datos'
	#posicion = getData()

	print "corregir angulos pan!!!!"
	
	
	#lat,lon=-38.834835,-72.698472 #poste1
	#lat,lon=-38.833929,-72.698461 #poste2
	#lat,lon=-38.832722,-72.698398 #poste 3 no coincide/no coincide
	#lat,lon=-38.833755,-72.699508 #poste 5
	#lat,lon=-38.834621,-72.699629 #punto 6 
	#lat,lon=-38.832674,-72.70066 #poste 7 no coincide/no coincide
	#lat,lon=-38.833777,-72.70078 #poste 8 no coincide/no coincide
	#lat,lon=-38.835504,-72.70199 #punto 9
	#lat,lon=-38.835660,-72.700070 #punto 10 arbol
	#lat,lon=-38.835717,-72.700986 #poste 11 cerca  no coincide
	#lat,lon=-38.838654, -72.701000 #poste12
	#lat,lon=-38.838820, -72.702915 #poste13
	lat,lon=-38.837749, -72.704183 #poste14
	#lat,lon=-38.836755, -72.708900
	

	#print (posicion['Latitud'],posicion['Longitud'])
	print lat,lon
	pan,distancia=seguimiento(lat,lon,ip1)
	print pan
	pan=interpolPan(pan)
	tilt=controlTilt(distancia)
	tilt=interpolTilt(distancia,ip1)

	zoom=interpolZoom(distancia)

	velocity=0.1 #velocidad camara
	vaca1.move_abspantilt(pan,tilt,zoom,velocity) #la precision del desplazamiento depende de la velocidad.
	
	vaca1.stop()
	
	

#Soli Deo Gloria
