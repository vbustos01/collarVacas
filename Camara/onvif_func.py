from time import sleep
from onvif import ONVIFCamera

ip = '192.168.0.64'
port = 80
user = 'admin'
passwd = 'fondef18I10360'
cam = ONVIFCamera(ip, port, user, passwd, '/home/vitocosmic/Escritorio/python-onvif/wsdl')
