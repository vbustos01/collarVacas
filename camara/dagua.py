#import urllib
#import cv2
#import numpy as np
#cam = cv2.VideoCapture()
#cam.open("rtsp://admin:ufro_ufro_ufro@192.168.1.109:554")
#while True:
#    r, f = cam.read()
    #gray =cv2.cvt.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#    cv2.imshow('IP Camera stream',f)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#cam.release()
#cv2.destroyAllWindows()

from onvif import ONVIFCamera

ip = '192.168.1.109'
port = 80
user = 'admin'
passwd = 'ufro_ufro_ufro'
cam = ONVIFCamera(ip, port, user, passwd, '/home/victor/collarvacas/camara/python-onvif/wsdl')
