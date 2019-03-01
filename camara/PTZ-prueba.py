"""
###############################################
programa info y movimiento basico de camara ptz

giros:

    Hikvision ptz:
        pan   = 0 - 360 (grados) -> [-1,1]
        tilt  = 0 - 90  (grados) -> [-1,1]
        zooon = 0.5 - 1
 

****
***** RECORDAR CAMBIAR DIRECCION WSDL
****

            CAMARA PTZ - ONVIF
###############################################
"""

from onvif import ONVIFCamera
from time import sleep

timeout=1



def accion_mover(ptz,peticion,timeout):
    ptz.ContinuousMove(peticion)
    sleep(timeout)
    ptz.Stop(peticion)

def move_up(ptz, peticion, timeout=1):
    print 'move up...'
    peticion.Velocity.PanTilt._x = 0
    peticion.Velocity.PanTilt._y = YMAX
    accion_mover(ptz,peticion,timeout)

def move_down(ptz, peticion, timeout=1):
    print 'move down...'
    peticion.Velocity.PanTilt._x = 0
    peticion.Velocity.PanTilt._y = YMIN
    accion_mover(ptz,peticion,timeout)

def move_right(ptz, peticion, timeout=1):
    print 'move right...'
    peticion.Velocity.PanTilt._x = XMAX
    peticion.Velocity.PanTilt._y = 0
    accion_mover(ptz,peticion,timeout)

def move_left(ptz, peticion, timeout=1):
    print 'move left...'
    peticion.Velocity.PanTilt._x = XMIN
    peticion.Velocity.PanTilt._y = 0
    accion_mover(ptz,peticion,timeout)

def zoom_in(ptz,peticion,timeout=1):
    print 'zoom in...'
    peticion.Velocity.Zoom._x    = ZMAX
    accion_mover(ptz,peticion,timeout)

def zoom_out(ptz,peticion,timeout=1):
    print 'zoom out...'
    peticion.Velocity.Zoom._x    = ZMIN
    accion_mover(ptz,peticion,timeout)

def status(ptz,peticion,timeout=0.5):
    estados= ptz.GetStatus({'ProfileToken': media_profile._token})

    positionX=estados.Position.PanTilt._x
    positionY=estados.Position.PanTilt._y
    zoom=estados.Position.Zoom._x

    info = cam.devicemgmt.GetHostname()
    fecha = cam.devicemgmt.GetSystemDateAndTime()
    print ("------------------------------------")
    print("posicion actual camara")
    print ("posicion x= ",positionX)
    print ("posicion y= ",positionY)
    print ("zoom = ",zoom)
    print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
    fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"
    print ("------------------------------------")
    sleep(timeout)


# instanciacion del objeto onvif
# _token = "Profile_1"
ip = '192.168.0.64'
port = 80
user = 'admin'
passwd = 'fondef18I10360'
cam = ONVIFCamera(ip, port, user, passwd, '/home/pedroc/Escritorio/python-onvif/wsdl')

# informacion de la camara
info = cam.devicemgmt.GetHostname()
fecha = cam.devicemgmt.GetSystemDateAndTime()
usr = cam.devicemgmt.GetUsers()

# print info camara
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
#search= cam.create_search_service()

media_profile = media.GetProfiles()[0] # profile


peticion = ptz.create_type('GetConfigurationOptions')
peticion.ConfigurationToken = media_profile.PTZConfiguration._token
ptz_config = ptz.GetConfigurationOptions(peticion)
peticion = ptz.create_type('ContinuousMove')
peticion.ProfileToken = media_profile._token
ptz.Stop({'ProfileToken': media_profile._token})


# rangos de la camara
global  XMAN,XMIN,YMAX,YMIN,ZMAX,ZMIN 
XMAX = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max # +1
XMIN = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min # -1
YMAX = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max # +1
YMIN = ptz_config.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min # -1
ZMAX = ptz_config.Spaces.ContinuousZoomVelocitySpace[0].XRange.Max    # +1
ZMIN = ptz_config.Spaces.ContinuousZoomVelocitySpace[0].XRange.Min    # -1

# movimiento manual (pain, tilt,zoom) --(X,Y,Z)
###################
#peticion.Velocity.PanTilt._x = 0#XMAX
#peticion.Velocity.PanTilt._y = 0#YMAX
#peticion.Velocity.Zoom._x    = 0#ZMAX
###################

#REVIEW POSICIONES CAMARA 

x=int(input("cuantas iteraciones : "))
for i in range(x):
    #move_left(ptz,peticion)
    #move_up(ptz,peticion)

#    status(ptz,peticion)

#    zoom_out(ptz,peticion)
    move_left(ptz,peticion)
#    move_down(ptz,peticion)


#request=search.create_type('FindPTZPosition')

#print peticion
#print peticion
#ptz.SetHomePosition({'ProfileToken': media_profile._token})
#sleep(2)
#ptz.GetConfigurations()

# ejemplo funcional de libreria ptz
#pt = cam.ptz.GetServiceCapabilities()


############### revision de atributos #################
############ comentar de ser necesario ################
#for i in dir(ONVIFCamera):
#   print i
