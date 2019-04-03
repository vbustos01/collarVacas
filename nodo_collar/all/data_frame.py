"""Modulo utilizado para paquetes de Información Red LoRa"""
def empaquetar(pre_frame):
	location = pre_frame['location'].split(',')
	simbLatitud = location[1] == 'S'
	simbLongitud= location[3] == 'W'
	Latitud = int(float(location[0])*10000)#(27bits)
	Longitud = int (float(location[2])*10000)#(28bits)
	paquete=bytearray(15)
	paquete[0]=pre_frame['address'] & 0xff #1 BYTE de direccion del collar
	paquete[1]=(pre_frame['cmd'] & 0x07)# 3 bits de Comandos
	x = 3
	for i in pre_frame['sensors'].values():
		paquete[1] |= i << x #4 bits para estado de sensores
		x += 1
	
	paquete[1] |= simbLatitud << 7 #Simbolo de la Latitud 1 bit
	for i in range(3):
		paquete[2+i] = (Latitud>>i*8) & 0xff

	paquete[5] = ((Latitud >> 24) & 0x07) | (simbLongitud << 3) | ((Longitud & 0x0F) << 4)
	for i in range(3):
		paquete[6+i] = (Longitud >> 4+i*8) & 0xff
	for i in range(4):
	 	paquete[9+i] = pre_frame['t_unix']>>i*8 & 0xff
	paquete[13] = pre_frame['bateria'] & 0xff
	paquete[14] = ((pre_frame['bateria'] >> 8) & 0x0F) | ((pre_frame['C_close'] & 0x0F) << 4) 
	return paquete

def desempaquetar(paquete):
	if len(paquete) == 15:
		
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
		Latitud = paquete[2] | (paquete[3] << 8) | (paquete[4] << 16) | ((paquete[5]&0x07) << 24)
		Longitud = (paquete[5]>>4) | (paquete[6] << 4) | (paquete[7] << 12) | (paquete[8]<< 20)
							  #signo							  #grados			    #minutos	
		pre_frame['location']=[(-1 if (paquete[1]>>7)&0x01 else 1),int(Latitud/1000000), float(Latitud % 1000000)/10000,#Latitud
							   (-1 if (paquete[5]>>3)&0x01 else 1),int(Longitud/1000000),float(Longitud % 1000000)/10000]#Longitud

		pre_frame['t_unix']  = paquete[9]  | (paquete[10] << 8) | (paquete[11] << 16) | (paquete[12]<<24)
		pre_frame['bateria'] = paquete[13] | ((paquete [14] & 0x0F) << 8)
		pre_frame['C_close'] = paquete[14] >> 4

	return pre_frame