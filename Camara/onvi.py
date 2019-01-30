from onvif import ONVIFCamera

# instanciacion del objeto onvif
ip = '192.168.0.64'
port = 80
user = 'admin'
passwd = 'fondef18I10360'
cam = ONVIFCamera(ip, port, user, passwd, '/home/vitocosmic/Escritorio/python-onvif/wsdl')

# informacion de la camara
info = cam.devicemgmt.GetHostname()
fecha = cam.devicemgmt.GetSystemDateAndTime()
usr = cam.devicemgmt.GetUsers()

# prints
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

# servicio media
media_serv = cam.create_media_service()
print media_serv.GetProfile()

# PTZ
ptz_serv = cam.create_ptz_service()
# ejemplo funcional de libreria ptz
#pt = cam.ptz.GetServiceCapabilities()

############### revision de atributos #################
############ comentar de ser necesario ################
#for i in dir(media_serv):
#	print i
