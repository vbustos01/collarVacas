import urllib
import cv2
import numpy as np

# camara hikvision
cam = cv2.VideoCapture()
#rtsp://admin:ufro_ufro_ufro@192.168.1.108
#ip = 'rtsp://admin:fondef18I10360@192.168.0.64:554/1'
cam.open("rtsp://admin:fondef18I10360@192.168.0.64:554/Streaming/channels/2/")
#cv2.imshow('camara 2', cam)
#cv2.waitKey()
while True:

    r, f = cam.read()
    #gray =cv2.cvt.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('IP Camera stream',f)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
