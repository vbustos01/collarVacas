

'''

latitud: mide de norte a suer
longitud: mide de oeste a este
'''

import numpy as np
import math

def controlPan(lat,lon):
	lat0,lon0=-38.835723,-72.700791

	latRef,lonRef=-38.833929,-72.698461 #referencia poste 2

	vec0=np.array([lat0,lon0]) #posicion poste origen
	vec1=np.array([lat,lon])  #poste8 
	vec2=np.array([latRef,lonRef])  



	vec0=np.flip(vec0)
	vec1=np.flip(vec1)
	vec2=np.flip(vec2)


	vec1=(vec1-vec0)
	vec2=(vec2-vec0)

	a=math.atan2(vec1[1],vec1[0])
	r=0.895-0.903

	offset=math.atan2(vec2[1],vec2[0])+0.04
	#offset= #0.895-0.883594299849


	a=a-offset
	print a
	if a>0:
		a=1-a/(math.pi) 
	if a<0:
		a=-(1+a/(math.pi))

	a= a-0.012
	print a



	return a

