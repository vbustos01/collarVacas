from math import sqrt,sin,cos,asin,pi,acos,degrees,atan2,hypot,fabs
from numpy import sign
import pickle

#funcion para calcular la distancia entre dos coordenadas de GPS
def haversine(lat1,lon1,lat2,lon2):
		rad=pi/180
		dlat=lat2-lat1
		dlon=lon2-lon1
		R=6372.795477598 #"kilometros"

		a=(sin(rad*dlat/2))**2 + cos(rad*lat1)*cos(rad*lat2)*(sin(rad*dlon/2))**2 
		distancia=2*R*asin(sqrt(a))*1000 #metros
		return distancia

def seguimiento(lat,lon):

	latCam,lonCam = -38.835831, -72.702263 #coordenada fija de la camara
	latOrigen,lonOrigen = -38.837626, -72.704261 #coordenada donde apunta el origen de la camara
	latm9,lonm9=-38.835339, -72.705240 #coordenada angulo -90 grados
	lat, lon  #posicion llegada del collar
	
	a=haversine(lat,lon,latOrigen,lonOrigen) #collar-origen
	b=haversine(latCam,lonCam,latOrigen,lonOrigen) #camara-origen
	c=haversine(latCam,lonCam,lat,lon) #camara-collar

	#referencia -90 grados
	d=haversine(latCam,lonCam,latm9,lonm9) #camara-ref2
	e=haversine(lat,lon,latm9,lonm9) #collar-ref2	
	print 'distancia ->collar-origen:',a
	print 'distancia ->camara-origen:',b
	print 'distancia ->camara-collar:',c

	print 'distancia ->collar-ref2:',d
	print 'distancia ->camara-ref2:',e


	#pan
	if c!=0:
		beta=acos((-(e**2)+d**2+c**2)/(2*d*c)) #codicion

		if beta<pi/2:
			alfa=acos((-(a**2)+b**2+c**2)/(2*b*c)) 
		else:
			alfa=-acos((-(a**2)+b**2+c**2)/(2*b*c))

		print degrees(alfa),'grados, desde el origen'

		pan=alfa/pi #paramatros listo
		pan_ant=pan

	else:
		pan=pan_ant

	return pan,c




def controlTiltZoom(distancia):

	distancia = float(distancia)

	a=(distancia*19/500)
	a=round(a)

	print a


	if(a==0):
		zoom,tilt=0,-0.529091
	if(a==1):
		zoom,tilt=0,-0.36
	if(a==2):
		zoom,tilt=0.015625,-0.109091
	if(a==3):
		zoom,tilt=0.015625,0.04
	if(a==4):
		zoom,tilt=0.046875,0.170909
	if(a==5):
		zoom,tilt=0.054688,0.309091
	if(a==6):
		zoom,tilt=0.109375,0.347273
	if(a==7):
		zoom,tilt=0.164062,0.38
	if(a==8):
		zoom,tilt=0.195312,0.412727
	if(a==9):
		zoom,tilt=0.234375,0.425455
	if(a==10):
		zoom,tilt=0.234375,0.443636
	if(a==11):
		zoom,tilt=0.273438,0.454545
	if(a==12):
		zoom,tilt=0.3125,0.472727 
	if(a==13):
		zoom,tilt=0.429688,0.481818
	if(a==14):
		zoom,tilt=0.429688,0.487273
	if(a==15):
		zoom,tilt=0.507812,0.496364
	if(a==16):
		zoom,tilt=0.59375,0.501818 
	if(a==17):
		zoom,tilt=0.671875,0.503636
	if(a==18):
		zoom,tilt=1.0,0.507273
	if(a==19):
		zoom,tilt=1.0,0.510909 


	print zoom,tilt


def getData():
	
	archivo=open('/home/pi/collarVacas/raspberry/vaca_ID1.dat','rb')
	diccionario=pickle.load(archivo)
	archivo.close
	return diccionario



