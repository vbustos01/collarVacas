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
from time import sleep,strftime

timeout=1

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
print "fecha: {}/{}/{}".format(str(fecha.UTCDateTime.Date.Day),
    fecha.UTCDateTime.Date.Month, fecha.UTCDateTime.Date.Year) + "\n"
print "hora: {}:{}:{}".format(str(fecha.UTCDateTime.Time.Hour),
    fecha.UTCDateTime.Time.Minute, fecha.UTCDateTime.Time.Second) + "\n"
########################################################################

media = cam.create_media_service()
ptz = cam.create_ptz_service()


media_profile = media.GetProfiles()[0] # profile


fecha=strftime("%x")
hora=strftime("%X")



params = cam.devicemgmt.create_type('SetHostname')
params.Hostname = 'NewHostName'
cam.devicemgmt.SetHostname(params)

time_params = cam.devicemgmt.create_type('SetSystemDateAndTime')
time_params.DateTimeType = 'Manual'
time_params.DaylightSavings = True
time_params.TimeZone.TZ = 'CST+00:00:00'
time_params.UTCDateTime.Date.Year = 2000+int(fecha[6:8])
time_params.UTCDateTime.Date.Month = int(fecha[0:2])
time_params.UTCDateTime.Date.Day = int(fecha[3:5])
time_params.UTCDateTime.Time.Hour = int(hora[0:2])
time_params.UTCDateTime.Time.Minute = int(hora[3:5])
time_params.UTCDateTime.Time.Second = int(hora[6:8])
cam.devicemgmt.SetSystemDateAndTime(time_params)