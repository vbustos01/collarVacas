from math import sqrt,sin,cos,asin,pi,acos,degrees,atan2,hypot,fabs
from numpy import sign
import pickle
import math

#funcion para calcular la distancia entre dos coordenadas de GPS
def haversine(lat1,lon1,lat2,lon2):
		rad=pi/180
		dlat=lat2-lat1
		dlon=lon2-lon1
		R=6372.795477598 #"kilometros"

		a=(sin(rad*dlat/2))**2 + cos(rad*lat1)*cos(rad*lat2)*(sin(rad*dlon/2))**2 
		distancia=2*R*asin(sqrt(a))*1000 #metros
		return distancia

def seguimiento(lat,lon,ip):

	if(ip=='172.22.120.193'):
		latCam,lonCam =-38.835723, -72.700791 #coordenada fija de la camara
		latOrigen,lonOrigen = -38.837665, -72.703433 #coordenada donde apunta el origen de la camara
		#-38.837626, -72.704261 anterior
		#-38.837665, -72.703433
		#latm9,lonm9=-38.835339, -72.705240 #coordenada angulo 90 grados
		latm9,lonm9=-38.835061, -72.701736 #coordenada angulo 90 grados		

		lat, lon  #posicion llegada del collar

		a=haversine(lat,lon,latOrigen,lonOrigen) #collar-origen
		b=haversine(latCam,lonCam,latOrigen,lonOrigen) #camara-origen
		c=haversine(latCam,lonCam,lat,lon) #camara-collar

		#referencia -90 grados
		d=haversine(latCam,lonCam,latm9,lonm9) #camara-ref2
		e=haversine(lat,lon,latm9,lonm9) #collar-ref2
		#print 'distancia ->collar-origen:',a
		#print 'distancia ->camara-origen:',b
		print 'distancia ->camara-collar:',c

		#print 'distancia ->collar-ref2:',d
		#print 'distancia ->camara-ref2:',e

		pan_ant=1
		#pan
		if c!=0:
			beta=acos((-(e**2)+d**2+c**2)/(2*d*c)) #codicion

			if beta<pi/2:
				alfa=acos((-(a**2)+b**2+c**2)/(2*b*c))
			else:
				alfa=-acos((-(a**2)+b**2+c**2)/(2*b*c))

			#print degrees(alfa),'grados, desde el origen'

			pan=alfa/pi #
			pan_ant=pan

		else:
			pan=pan_ant

		if pan <1 and pan>0.5:
			pan=pan-0.002440430577 #offset en sentido antihorario
		if pan<0.5 and pan>0:
			pan=pan+0.013334 #offset en sentido antihorario
		if pan>-0.5 and pan<0:
			pan=pan+0.0110546 #offset en sentido horario
	 	if pan >-0.99 and pan<-0.5:
			pan=pan+0.00965#offset en sentido antihorario
		if pan >-1 and pan<-0.99:
			pan=pan-0.0114 #offset caso especial
		if pan<-1:
			pan=2+pan



	if(ip=='172.22.120.194'):
		latCam,lonCam =-38.835723, -72.700791 #coordenada fija de la camara
		latOrigen,lonOrigen = -38.835061, -72.701736 #coordenada donde apunta el origen de la camara
		latm9,lonm9=-38.834049, -72.698538 #coordenada angulo 90 grados
		lat, lon  #posicion llegada del collar

		a=haversine(lat,lon,latOrigen,lonOrigen) #collar-origen
		b=haversine(latCam,lonCam,latOrigen,lonOrigen) #camara-origen
		c=haversine(latCam,lonCam,lat,lon) #camara-collar

		#referencia 90 grados
		d=haversine(latCam,lonCam,latm9,lonm9) #camara-ref2
		e=haversine(lat,lon,latm9,lonm9) #collar-ref2
		#print 'distancia ->collar-origen:',a
		#print 'distancia ->camara-origen:',b
		
		print 'distancia ->camara-collar:',c

		#print 'distancia ->collar-ref2:',d
		#print 'distancia ->camara-ref2:',e
		pan_ant=1
		#pan
		if c!=0:
			beta=acos((-(e**2)+d**2+c**2)/(2*d*c)) #codicion

			if beta<pi/2:
				alfa=acos((-(a**2)+b**2+c**2)/(2*b*c))
			else:
				alfa=-acos((-(a**2)+b**2+c**2)/(2*b*c))

			#print degrees(alfa),'grados, desde el origen'

			pan=alfa/pi #paramatros listo
			pan_ant=pan

		else:
			pan=pan_ant

		'''	
		if pan <1 and pan>0.5:
			pan=pan-0.002440430577 #offset en sentido antihorario
		if pan<0.5 and pan>0:
			pan=pan+0.013334 #offset en sentido antihorario
		if pan>-0.5 and pan<0:
			pan=pan+0.0110546 #offset en sentido horario
	 	if pan >-0.99 and pan<-0.5:
			pan=pan+0.00965#offset en sentido antihorario

		if pan >-1 and pan<-0.99:
			pan=pan-0.0114 #offset caso especial
		if pan<-1:
			print "gg"
			pan=2+pan
		'''	



	return pan,c



def controlZoom(distancia):

	#distancia de 0-500
	#zoom 0-1
	if distancia>=250:
		distancia=250

	z=distancia/250

	return z

def controlTilt(x):
	#distancia de 0-500
	#tilt -0.52 -- 0.52
	y=(3e-8)*x**3 - (2e-5)*x**2 + (0.0053)*x+ 0.0791



	return y


def getData():
	
	archivo=open('/home/pi/datos/vaca_ID1.dat','rb')
	diccionario=pickle.load(archivo)
	archivo.close
	return diccionario

