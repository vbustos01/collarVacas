from onvif import ONVIFCamera
from time import sleep

# ejemplo de las coordenadas:
# 3844.7556,S,07236.9213,W

def video_signal():
	import cv2
	cam = cv2.VideoCapture()
	cam.open("rtsp://admin:ufro_ufro_ufro@192.168.1.109:554")
	try:
		while True:
		    r, f = cam.read()
		    cv2.imshow('IP Camera stream',f)
		    if cv2.waitKey(1) & 0xFF == ord('q'):
		        break
	except KeyboardInterrupt:
		cam.release()
		cv2.destroyAllWindows()
	except:
		print "error desconocido"

def info_cam():
	# zona horaria de chile GTM: -4:00
	# informacion de la camara
	info = cam.devicemgmt.GetHostname()
	fecha = cam.devicemgmt.GetSystemDateAndTime()
	usr = cam.devicemgmt.GetUsers()

	print "Informacion de la camara:\n"
	print "nombre de la camara: " + str(info.Name) + "\n"
	print "zona horaria: " + str(fecha.TimeZone) + "\n"
	print "year: " + str(fecha.UTCDateTime.Date.Year) + "\n"
	print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
	fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"
###################################################################################
XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1

def perform_move(ptz, request, timeout):
    # Start continuous move
    ptz.ContinuousMove(request)
    # Wait a certain time
    sleep(timeout)
    # Stop continuous move
    ptz.Stop({'ProfileToken': request.ProfileToken})

def move_up(ptz, request, timeout=1):
    print 'move up...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMAX
    perform_move(ptz, request, timeout)

def move_down(ptz, request, timeout=1):
    print 'move down...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMIN
    perform_move(ptz, request, timeout)

def move_right(ptz, request, timeout=1):
    print 'move right...'
    request.Velocity.PanTilt._x = XMAX
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)

def move_left(ptz, request, timeout=1):
    print 'move left...'
    request.Velocity.PanTilt._x = XMIN
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)
#######################################################################################
def continuous_move():
	ip = '192.168.1.109'
	port = 80
	user = 'admin'
	passwd = 'ufro_ufro_ufro'
	cam = ONVIFCamera(ip, port, user, passwd, '/home/victor/collarvacas/camara/python-onvif/wsdl')
	media = cam.create_media_service()
	ptz = cam.create_ptz_service()
	media_profile = media.GetProfiles()[0];

	# Get PTZ configuration options for getting continuous move range
	request = ptz.create_type('GetConfigurationOptions')
	request.ConfigurationToken = media_profile.PTZConfiguration._token
	ptz_configuration_options = ptz.GetConfigurationOptions(request)

	request = ptz.create_type('ContinuousMove')
	request.ProfileToken = media_profile._token
	ptz.Stop({'ProfileToken': media_profile._token})

	# Get range of pan and tilt
	# NOTE: X and Y are velocity vector
	global XMAX, XMIN, YMAX, YMIN
	XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
	XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
	YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
	YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

	return [ptz,request]

	# move right
	#move_right(ptz, request)
	# move left
	#move_left(ptz, request)
	# Move up
	#move_up(ptz, request)
    # move down
	#move_down(ptz, request)
##########################################################################################


# video
#video_signal()

# movimiento
continuous_move()

move_right(ptz, request)
# f(x) check
#for i in dir(ptz):
#	print i