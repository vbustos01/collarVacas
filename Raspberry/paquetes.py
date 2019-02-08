"""Modulo utilizado para paquetes de Información Red LoRa"""
def empaquetar(pre_frame):

	location = pre_frame['location'].split(',')
	simbLongitud = location[1] == 'S'
	simbLatitud= location[3] == 'W'
	Longitud = int(float(location[0])*10000)#(27bits)
	Latitud = int (float(location[2])*10000)#(28bits)
	paquete=bytearray(15)
	paquete[0]=pre_frame['address'] & 0xff #1 BYTE de direccion del collar
	paquete[1]=(pre_frame['cmd'] & 0x07)# 3 bits de Comandos
	x = 3
	for i in pre_frame['sensors'].values():
		paquete[1] |= i << x #4 bits para estado de sensores
		x += 1
	
	paquete[1] |= simbLongitud << 7 #Simbolo de la Longitud 1 bit
	for i in range(3):
		paquete[2+i] = (Longitud>>i*8) & 0xff

	paquete[5] = ((Longitud >> 24) & 0x07) | (simbLatitud << 3) | ((Latitud & 0x0F) << 4)
	for i in range(3):
		paquete[6+i] = (Latitud >> 4+i*8) & 0xff
	for i in range(4):
	 	paquete[9+i] = pre_frame['t_unix']>>i*8 & 0xff
	paquete[13] = pre_frame['bateria'] & 0xff
	paquete[14] = ((pre_frame['bateria'] >> 8) & 0x0F) | ((pre_frame['C_close'] & 0x0F) << 4) 
	return paquete
def desempaquetar(paquete):
	if len(paquete) == 15
		
		sensors     = {'GPS':None,'IMU':None,'SD':None,'MIC':None}
		pre_frame   ={'address':None,'cmd':None,
					'sensors':sensors,'location':None,
					't_unix':None,'bateria':None,'C_close':None}
		
		pre_frame['address'] = paquete[0]
		pre_frame['cmd']     = paquete[1] & 0x07
		x = 3
		for i in pre_frame['sensors'].keys():
			pre_frame['sensors'][i]=bool((paquete[1]>>x)&0x01) #4 bits para estado de sensores
			x += 1

	return pre_frame
	
	

sensors = {'GPS':True,'IMU':True,'SD':True,'MIC':True}
pre_frame ={'address':10,'cmd':0,
			'sensors':sensors,'location':"4212.7845,N,7845.4122,W",
			't_unix':1549624324,'bateria':145,'C_close':True}
dato=empaquetar(pre_frame)
print('tam:',len(dato))
