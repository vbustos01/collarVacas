from time import sleep
from onvif import ONVIFCamera

def mover(ptz, peticion, tiempo):
	ptz.ContinuousMove(peticion)
	sleep(tiempo)
	ptz.stop({'ProfileToken': peticion.ProfileToken})

def mov_arriba(ptz, dist, peticion, tiempo):
	peticion.Velocity.PanTilt._x = 0
	peticion.Velocity.PanTilt._y = dist
	mover(ptz, peticion, tiempo)

def movimiento_continuo():
	ip = '192.168.0.64'
	port = 80
	user = 'admin'
	passwd = 'fondef18I10360'
	cam = ONVIFCamera(ip, port, user, passwd, '/home/vitocosmic/Escritorio/python-onvif/wsdl')
	
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

	mov_arriba(ptz, YMAX, peticion, 1)

movimiento_continuo()