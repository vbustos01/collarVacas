# -*- coding: utf-8 -*-
"""
###############################################
programa info y movimiento basico de camara ptz


giros:

    Hikvision ptz:
        pan   = 0 - 360 (grados) -> [-1,1]
        tilt  = 90 - 0  (grados) -> [-1,1]
        zooon = 0.5 - 1
 


            CAMARA PTZ - ONVIF
###############################################
"""
from onvif import ONVIFCamera
from time import sleep,strftime
from math import sqrt,sin,cos,asin,pi,acos,degrees,atan2,hypot
import sys
import random
import utm 

to=0.1 #el paso entre cada movimiento

#funciones para mover la camara en todas direcciones incluyendo zoom
def accion_mover(ptz,peticion,timeout=to):
    ptz.ContinuousMove(peticion)
    sleep(timeout)

def move_up(ptz, peticion, timeout=to):
    print 'move up...'
    peticion.Velocity.PanTilt._x = 0
    peticion.Velocity.PanTilt._y = YMAX
    accion_mover(ptz,peticion,timeout)

def move_down(ptz, peticion, timeout=to):
    print 'move down...'
    peticion.Velocity.PanTilt._x = 0
    peticion.Velocity.PanTilt._y = YMIN
    accion_mover(ptz,peticion,timeout)

def move_right(ptz, peticion, timeout=to):
    print 'move right...'
    peticion.Velocity.PanTilt._x = XMAX
    peticion.Velocity.PanTilt._y = 0
    accion_mover(ptz,peticion,timeout)

def move_left(ptz, peticion, timeout=to):
    print 'move left...'
    peticion.Velocity.PanTilt._x = XMIN
    peticion.Velocity.PanTilt._y = 0
    accion_mover(ptz,peticion,timeout)

def zoom_in(ptz,peticion,timeout=to):
    print 'zoom in...'
    peticion.Velocity.Zoom._x    = ZMAX
    accion_mover(ptz,peticion,timeout)

def zoom_out(ptz,peticion,timeout=to):
    print 'zoom out...'
    peticion.Velocity.Zoom._x    = ZMIN
    accion_mover(ptz,peticion,timeout)

#funcion para mostrar la posicion en la que se encuentra cada variable de la camara 
def status(ptz,peticion,timeout=0.01):
    estados= ptz.GetStatus({'ProfileToken': media_profile._token})

    positionX=estados.Position.PanTilt._x
    positionY=estados.Position.PanTilt._y
    zoom=estados.Position.Zoom._x

    info = cam.devicemgmt.GetHostname()
    fecha = cam.devicemgmt.GetSystemDateAndTime()
    print ("------------------------------------")
    print("posicion actual camara")
    print ("posicion pan= ",positionX)
    print ("posicion tilt= ",positionY)
    print ("zoom = ",zoom)
    print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
    fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"
    print ("------------------------------------")
    sleep(timeout)

    return positionX,positionY,zoom

def actualizarFecha(cam):
	fecha=strftime("%x")
	hora=strftime("%X")
	params = cam.devicemgmt.create_type('SetHostname')
	params.Hostname = 'NewHostName'
	cam.devicemgmt.SetHostname(params)

	time_params = cam.devicemgmt.create_type('SetSystemDateAndTime')
	time_params.DateTimeType = 'Manual'
	time_params.DaylightSavings = True
	time_params.TimeZone.TZ = 'CST+00:00:00'
	time_params.UTCDateTime.Date.Year = 2000+int(fecha[6:8])
	time_params.UTCDateTime.Date.Month = int(fecha[0:2])
	time_params.UTCDateTime.Date.Day = int(fecha[3:5])
	time_params.UTCDateTime.Time.Hour = int(hora[0:2])
	time_params.UTCDateTime.Time.Minute = int(hora[3:5])
	time_params.UTCDateTime.Time.Second = int(hora[6:8])
	cam.devicemgmt.SetSystemDateAndTime(time_params)

def mod(a):
	return sqrt(a**2)

#funcion para calcular la distancia entre dos coordenadas de GPS
def haversine(lat1,lon1,lat2,lon2):
		rad=pi/180
		dlat=lat2-lat1
		dlon=lon2-lon1
		R=6372.795477598 #"kilometros"

		a=(sin(rad*dlat/2))**2 + cos(rad*lat1)*cos(rad*lat2)*(sin(rad*dlon/2))**2 
		distancia=2*R*asin(sqrt(a))*1000 #metros
		return distancia
#funcion para ingresar coordenadas gps y convertir a las coordenadas propias de la camara ptz
def input_conversion():
	lat, lon=-38.746830, -72.615908
	print lat,lon
	latCam,lonCam=-38.746171, -72.615092 #posicion fija de la camara


	distancia=haversine(lat,lon,latCam,lonCam)
	disx=haversine(lat,lonCam,latCam,lonCam)

	print distancia #distancia total entre camara y objetivo(sin considerar altura)
	#3
	if lat<latCam and lon<lonCam:
		print 3
		angulo=-pi/2-(acos(disx/distancia))	
	#2
	if lat>latCam and lon<lonCam:
		print 2
		angulo=pi/2+(acos(disx/distancia))
	#4
	if lat<latCam and lon>lonCam:
		print 4
		angulo=-(acos(disx/distancia))
	#1
	if lat>latCam and lon>lonCam:
		print 1
		angulo=(acos(disx/distancia))
		print degrees(angulo)

	x=distancia*cos(angulo) #distancia en x hasta el objetivo
	y=distancia*sin(angulo) #distancia en y hasta el objetivo
	z=0  #altura en que se encuentra la camara

	h=hypot(z,distancia)
	angY=acos(z/h)

	refx=angulo/pi
	refy=-2*angY/(pi/2)+1
	refz=0.5

	return refx,refy,refz
######################################################################################################################################################

# instanciacion del objeto onvif
# _token = "Profile_1"

ip = '192.168.0.64'
port = 80
user = 'admin'
passwd = 'fondef18I10360'
cam = ONVIFCamera(ip, port, user, passwd, '/home/pedroc/Escritorio/python-onvif/wsdl')

actualizarFecha(cam)
# informacion de la camara
info = cam.devicemgmt.GetHostname()
fecha = cam.devicemgmt.GetSystemDateAndTime()
usr = cam.devicemgmt.GetUsers()

# print info camara
print "Informacion de la camara:\n"
print "nombre de la camara: " + str(info.Name) + "\n"
print "zona horaria: " + str(fecha.TimeZone) + "\n"
print "year: " + str(fecha.UTCDateTime.Date.Year) + "\n"
print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
    fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"
########################################################################

for i in usr:
    print i

# protocolos utilizados
proto = cam.devicemgmt.GetNetworkProtocols()
for i in proto:
    print i

media = cam.create_media_service()
ptz = cam.create_ptz_service()


media_profile = media.GetProfiles()[0] # profile

peticion = ptz.create_type('GetConfigurationOptions')
peticion.ConfigurationToken = media_profile.PTZConfiguration._token
ptz_config = ptz.GetConfigurationOptions(peticion)
peticion = ptz.create_type('ContinuousMove')
peticion.ProfileToken = media_profile._token
ptz.Stop({'ProfileToken': media_profile._token})


# rangos de la camara
global  XMAN,XMIN,YMAX,YMIN,ZMAX,ZMIN 

speed=0.8
XMAX = speed*ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max # +1 (hikvision)
XMIN = speed*ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min # -1 (hikvision)
YMAX = speed*ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max # +1 (hikvision)
YMIN = speed*ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min # -1 (hikvision)
ZMAX = speed*ptz_config.Spaces.ContinuousZoomVelocitySpace[0].XRange.Max    # +1 (hikvision)
ZMIN = speed*ptz_config.Spaces.ContinuousZoomVelocitySpace[0].XRange.Min    # -1 (hikvision)



###############################################################
########################## MAIN ###############################
############################################################### 
try:
#while True:
	positionX,positionY,zoom =status(ptz,peticion) #posicion actual de la camara
	refx,refy,refz=input_conversion() #posicion del objetivo

	#########

	#
	if (refx==0) and (refy!=0):
		refx=0.001
	if (refy==0) and (refx!=0):
		refy=0.001

	#error maaximo x

	if refx>=0.95:
		refx=0.95
		move_left(ptz,peticion)

	if refx<=-0.95:
		refx=-0.95

	if refy>1:
		refy=1

	print "\n"


	"""
	funcionamiento busqueda:
		-el programa cuenta con 16 posibles estados de las cuatro variables de interes (posicion camara= pan y tilt y posicion objetivo= pan y tilt)
		-tambien cuenta con 5 estados adicionales en donde el tilt tiende a ser maximo o la posicion del objetivo es el (0,0) de la camara
		-cada estado esta tomado de tal forma de cumplir con las peticiones 
		-se intento cubrir la mayoria de problemas presentados tales como el origen y en los maximos de pan y tilt
	
	"""
	while positionX<refx-0.1 or positionX>refx+0.1 or positionY<refy-0.1 or positionY>refy+0.1 : 

	###############    TODOS POSITIVOS   ##############################
		if (positionX>0) and (refx>0) and (positionY>0) and (refy>0):

			print refx,refy
			print 'TODOS POSITIVOS'

			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)		
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)	
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY) and (refx==0.001 or refy==0.001):
				if (positionX>0) and (refx==0.001):
					move_right(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY>0) and (refy==0.001):
					move_down(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionX<0) and (refx==0.001):
					move_left(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY<0) and (refy==0.001):
					move_up(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)				
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break
				
	##############      TODOS NEGATIVOS   #############################	
		if (positionX<0) and (refx<0) and (positionY<0) and (refy<0):

			print refx,refy
			print 'TODOS NEGATIVOS'

			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				
	############# CAMX Y REFY POSITIVOS ##################################
		if (positionX>0) and (refx<0) and (positionY<0) and (refy>0):
			print 'CAMx y refy POSITIVO'
			move_left(ptz,peticion)
			move_up(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

	############# CAMy Y REFx POSITIVOS ##################################
		if (positionX<0) and (refx>0) and (positionY>0) and (refy<0):
			print 'CAMx y refy POSITIVO'
			move_right(ptz,peticion)
			move_down(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

	################# los X POSITIVO      #######################################
		if (positionX>0) and (refx>0) and (positionY<0) and (refy<0):
			print refx,refy
			print 'LOS X POSITIVOS'
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)				
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)			
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)		
				positionX,positionY,zoom =status(ptz,peticion)
				
	################ los Y POSITIVO      #######################################
		if (positionX<0) and (refx<0) and (positionY>0) and (refy>0):
			print refx,refy
			print 'LOS Y POSITIVOS'
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)>sqrt(positionX*positionX) and sqrt(refy*refy)>sqrt(positionY*positionY):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO refx POSITIVA ####################################
		if (positionX<0) and (refx>0) and (positionY<0) and (refy<0):

			print refx,refy
			print 'CAMx NEGATIVO - CAMy NEGATIVO - refx POSITIVO - refy NEGATIVO'
			move_left(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)
			#caso si refx es cero
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY) and (refx==0.001):
				print("positivos - caso cero")
				if (positionX>0) and (refx==0.001):
					move_right(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY>0) and (refy==0.001):
					move_down(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionX<0) and (refx==0.001):
					move_left(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY<0) and (refy==0.001):
					move_up(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)	
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break

		############# SOLO POSICION CAMARAX POSITIVA #########################
		if (positionX>0) and (refx<0) and (positionY<0) and (refy<0):	
			print refx,refy
			print 'CAMx POSITIVO - CAMy NEGATIVO - refx NEGATIVO - refy NEGATIVO'
			move_right(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO POSICION CAMARAY POSITIVA #########################
		if (positionX<0) and (refx<0) and (positionY>0) and (refy<0):	
			print refx,refy
			print 'CAMY NEGATIVO - CAMy POSITIVO -refx NEGATIVO - refy NEGATIVO'
			move_down(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO refy POSITIVA ####################################
		if (positionX<0) and (refx<0) and (positionY<0) and (refy>0):
			print refx,refy
			print 'CAMx NEGATIVO - CAMy NEGATIVO - refx NEGATIVO - refy POSITIVO'
			move_up(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY) and (refy==0.001):
				print("caso cero")
				if (positionX>0) and (refx==0.001):
					move_right(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY>0) and (refy==0.001):
					move_down(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionX<0) and (refx==0.001):
					move_left(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY<0) and (refy==0.001): 
					move_up(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)			
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break

	#################### SOLO CAM NEGATIVA   ########################## 
		if (positionX<0) and (refx>0) and (positionY<0) and (refy>0):
			print 'CAMx NEGATIVO - CAMy NEGATIVO - refx POSITIVO - refy POSITIVO'
			move_left(ptz,peticion)
			move_up(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

	#################### SOLO REF NEGATIVA   ########################
		if (positionX>0) and (refx<0) and (positionY>0) and (refy<0):
			print 'refx NEGATIVO - refy NEGATIVO - CAMx POSITIVO - CAMy POSITIVO'
			move_right(ptz,peticion)
			move_down(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO refx NEGATIVA ####################################
		if (positionX>0) and (refx<0) and (positionY>0) and (refy>0):
			print refx,refy
			print 'CAMx POSITIVO - CAMy POSITIVO - refx NEGATIVO - refy POSITIVO'
			move_right(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO POSICION CAMARAX NEGATIVA #########################
		if (positionX<0) and (refx>0) and (positionY>0) and (refy>0):	
			print refx,refy
			print 'CAMx NEGATIVO - CAMy POSITIVO - refx POSITIVO - refy POSITIVO'
			move_left(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

		############# SOLO POSICION CAMARAY NEGATIVA #########################
		if (positionX>0) and (refx>0) and (positionY<0) and (refy>0):	
			print refx,refy
			print 'CAMY POSITIVO - CAMy NEGATIVO -refx POSITIVO - refy POSITIVO'
			move_up(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)


		############# SOLO refy NEGATIVA ####################################
		if (positionX>0) and (refx>0) and (positionY>0) and (refy<0):
			print refx,refy
			print 'CAMx POSITIVO - CAMy POSITIVO - refx POSITIVO - refy NEGATIVO'
			move_down(ptz,peticion)
			positionX,positionY,zoom =status(ptz,peticion)

#########################################################################
##### codicion especial cuando el la referencia del tilt es 1 o -1 ######


###############    TODOS POSITIVOS   ##############################
		if (positionX>0) and (refx>0) and (positionY>0) and (refy==1):
			print refx,refy
			print 'TODOS POSITIVOS y tilt = 1'
			while sqrt(refx*refx)<sqrt(positionX*positionX):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break			
			while sqrt(refx*refx)>sqrt(positionX*positionX) :
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break
				
	##############      TODOS NEGATIVOS   #############################	
		if (positionX<0) and (refx<0) and (positionY<0) and (refy==-1):
			print refx,refy
			print 'TODOS NEGATIVOS y tilt = -1'
			while sqrt(refx*refx)<sqrt(positionX*positionX):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_left(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break			
			while sqrt(refx*refx)>sqrt(positionX*positionX):
				if positionX<refx-0.09 or positionX>refx+0.09:
					move_right(ptz,peticion)
				if positionY<refy-0.09 or positionY>refy+0.09:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break

################# los X POSITIVO      #######################################
		if (positionX>0) and (refx>0) and (positionY<0) and (refy==-1):
			print refx,refy
			print 'LOS X POSITIVOS y tilt = -1'				
			while sqrt(refx*refx)<sqrt(positionX*positionX):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)			
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break
			while sqrt(refx*refx)>sqrt(positionX*positionX):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_down(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break			

	################ los Y POSITIVO      #######################################
		if (positionX<0) and (refx<0) and (positionY>0) and (refy==1):
			print refx,refy
			print 'LOS Y POSITIVOS y tilt = 1'
			while sqrt(refx*refx)<sqrt(positionX*positionX):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_left(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break
			while sqrt(refx*refx)>sqrt(positionX*positionX):
				if positionX<refx-0.1 or positionX>refx+0.1:
					move_right(ptz,peticion)
				if positionY<refy-0.1 or positionY>refy+0.1:
					move_up(ptz,peticion)
				positionX,positionY,zoom =status(ptz,peticion)
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break

	###############    REFERENCIA ORIGEN   ##############################
		if (((positionX<refx-0.1) or (positionX>refx+0.1)) or ((positionY>refy+0.1) or (positionY<refy-0.1))) and ((refx==0) and (refy==0)):
			print refx,refy
			print 'origen'
			while sqrt(refx*refx)<sqrt(positionX*positionX) and sqrt(refy*refy)<sqrt(positionY*positionY):
				print("caso cero")
				if (positionX>0) and (refx==0):
					move_right(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY>0) and (refy==0):
					move_down(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionX<0) and (refx==0):
					move_left(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)
				if (positionY<0) and (refy==0):
					move_up(ptz,peticion)
					positionX,positionY,zoom =status(ptz,peticion)	
				if positionX>refx-.1 and positionX<refx+.1 and positionY>refy-.1 and positionY<refy+.1:
					break

	print 'posicion encontrada'

except KeyboardInterrupt:
	ptz.Stop(peticion)
	sys.stdout.flush()
	sys.stderr.write("KeyboardInterrupt\n")

finally:
	print ("posicion requerida")
	print ("pan= ",refx)
	print ("tilt= ",refy)
	print ("zoom= ",refz)
	status(ptz,peticion)
	sys.stdout.flush()
	ptz.Stop(peticion)
	print("camara detenida")
   

##SDG