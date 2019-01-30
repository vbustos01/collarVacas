from onvif import ONVIFCamera

ip = '192.168.0.64'
port = 80
user = 'admin'
passwd = 'fondef18I10360'
cam = ONVIFCamera(ip, port, user, passwd, '/home/vitocosmic/Escritorio/python-onvif/wsdl')

# informacion de la camara
print "Informacion de la camara:\n"
info = cam.devicemgmt.GetHostname()
print "nombre de la camara: " + str(info.Name) + "\n"
fecha = cam.devicemgmt.GetSystemDateAndTime()
print "zona horaria: " + str(fecha.TimeZone) + "\n"
print "year: " + str(fecha.UTCDateTime.Date.Year) + "\n"
print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
	fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"

# protocolos utilizados
proto = cam.devicemgmt.GetNetworkProtocols()
for i in proto:
	print i

# PTZ
ptz_serv = cam.create_ptz_service()
# ejemplo funcional de libreria ptz
pt = cam.ptz.GetServiceCapabilities()



############### revision de atributos #################
############ comentar de ser necesario ################
#for i in dir(cam.ptz):
#	print i
