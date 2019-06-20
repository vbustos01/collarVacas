# -*- coding: utf-8 -*-

from ptz_cam import ptzcam
from time import sleep
from funciones_cam import seguimiento,controlTiltZoom,getData


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
#vaca2=ptzcam(ip2)

while True:

	#extrar posicion actual de la camara
	x=vaca1.status.Position.PanTilt._x # pan - eje horizontal
	y=vaca1.status.Position.PanTilt._y #tilt - eje vertical
	z=vaca1.status.Position.Zoom._x # zoom


	print 'posicion actual camara:', x,y,z
	# observacion! se dejo las variables como x,y,z por comodidad, pudiendo ser remplazadas en un futuro 


	#posicion requerida a apuntar
	print 'tomando datos'
	posicion = getData()

	pan, distancia = seguimiento(posicion['Latitud'],posicion['Longitud'],ip1)#lat,lon,ip
	#pan2, distancia2 = seguimiento(posicion['Latitud'],posicion['Longitud'],ip2)#lat,lon,ip

	zoom, tilt = controlTiltZoom(distancia)
	#zoom2, tilt2 = controlTiltZoom(distancia2)

	print "coordenada gps solicitada"
	print (posicion['Latitud'],posicion['Longitud'])


	velocity=0.3 #velocidad camara
	vaca1.move_abspantilt(pan,tilt,zoom,velocity) #la precision del desplazamiento depende de la velocidad.
	#vaca2.move_abspantilt(pan2,tilt2,zoom2,velocity) #la precision del desplazamiento depende de la velocidad.

	vaca1.stop()
	#vaca2.stop()

	print 'tiempo espera'
	sleep(10)

#Soli Deo Gloria
