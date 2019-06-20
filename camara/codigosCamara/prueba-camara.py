import pickle
from time import sleep
while True:
#    Latitud,Longitud=-38.837533, -72.704259         
    Latitud,Longitud=(input('ingrese coordenadas=').split(','))     

    Latitud,Longitud=float(Latitud),float(Longitud)

    #pickle.dump({'Latitud':Latitud,'Longitud':Longitud},open('vaca_ID1.dat','wb'),pickle.HIGHEST_PROTOCOL)
    pickle.dump({'Latitud':Latitud,'Longitud':Longitud},open('/home/pi/datos/vaca_ID1.dat','wb'),protocol=2)
    archivo=open('/home/pi/datos/vaca_ID1.dat','rb')
    diccionario=pickle.load(archivo)
    archivo.close
    print (diccionario)
    sleep(10)
