from math import sqrt,sin,cos,asin,pi,acos,degrees,atan2,hypot,fabs
from numpy import sign

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
	lat, lon=-38.746766, -72.615437
	print 'coordenada a apuntar'
	print lat,lon
	latCam,lonCam=-38.746197,-72.615089 #posicion fija de la camara

	t=-0.0003
	lineaRef = haversine(latCam+t,lonCam+t,latCam,lonCam)
	distancia=haversine(lat,lon,latCam,lonCam)

	print lineaRef
	
	disx=haversine(lat,lonCam,latCam,lonCam)


	print distancia #distancia total entre camara y objetivo(sin considerar altura)
	#print disx

	ang=acos(lineaRef/distancia)
	print ang
	print 'hola'
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

	print angulo
	
	x=distancia*cos(angulo) #distancia en x hasta el objetivo
	y=distancia*sin(angulo) #distancia en y hasta el objetivo
	z=0  #altura en que se encuentra la camara

	h=hypot(z,distancia)
	angY=acos(z/h)

	refx=angulo/pi
	refy=-2*angY/(pi/2)+1
	refz=0.5

	return refx,refy,refz



input_conversion()