from onvif import ONVIFCamera
from time import sleep

# instanciacion del objeto onvif
# _token = "Profile_1"
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
XMAX = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
XMIN = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
YMAX = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
YMIN = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

# movimiento
peticion.Velocity.PanTilt._x = XMAX
peticion.Velocity.PanTilt._y = 0
ptz.ContinuousMove(peticion)
sleep(2)
ptz.Stop({'ProfileToken': peticion.ProfileToken})

print("jeje")
# ejemplo funcional de libreria ptz
#pt = cam.ptz.GetServiceCapabilities()


############### revision de atributos #################
############ comentar de ser necesario ################
#for i in dir(media_serv):
#	print i
