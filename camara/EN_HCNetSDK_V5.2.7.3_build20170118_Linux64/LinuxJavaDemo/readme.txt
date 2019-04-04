Demo java build version JDK1.8

method one£º 
add netsdk lib to /usr/lib, then copy the lib in HCNetSDKCom to the  file directory /usr/lib

method two:
Modify ld.so.conf file in the directory /etc. Add the path to the so file you need for your Java project. Then call the ldconfig command to enable the configuration to take effect