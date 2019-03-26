from onvif import ONVIFCamera
from time import sleep

ip = '192.168.1.109'
port = 80
user = 'admin'
passwd = 'ufro_ufro_ufro'
cam = ONVIFCamera(ip, port, user, passwd, '/home/victor/collarvacas/camara/python-onvif/wsdl')
# media objects
media = cam.create_media_service()
ptz = cam.create_ptz_service()

media_profile = media.GetProfiles()[0]