## Collar

Proyecto

## Instalacion del firmware en la tarjeta
Para poder trabajar con la interfaz ESP32 el usuario debe contar con ciertos permisos para escribir sobre el puerto en el cual esta conectada la placa, en este caso ttyUSB0
```
sudo adduser MyUser dialout
sudo chmod a+rw /dev/ttyUSB0
```
NOTA: se debe modificar MyUser por el nombre de usuario respectivo.

Para revisar el puerto al cual esta conectada la placa se debe de hacer uso del siguiente comando:
```
dmesg | grep tty
```

El firmware de micropython se puede bajar de la pagina http://micropython.org/download#esp32 y su instalacion se realiza mediante la herramienta esptool, la cual puede obtenerse del repositorio oficial https://github.com/espressif/esptool , la instalacion procede de la siguiente forma:

Borrar firmware anterior:

```
esptool.py --chip esp32 -p /dev/ttyUSB0 erase_flash	
```
instalar firmware (se debe modificar tanto el puerto como el .bin en caso de ser necesario)
```
esptool.py --chip esp32 -p /dev/ttyUSB0 write_flash -z 0x1000 esp32-20190107-v1.9.4-773-gafecc124e.bin
```
## Modificar ficheros dentro de la tarjeta
Antes de instalar ampy se recomienda cambiar los permisos de acceso a la carpeta donde estan ubicadas las librerias de python mediante el siguiente comando:
```
sudo chmod -drwx /home/USUARIO/.local/lib
```
Para poder subir o ejecutar ficheros se utiliza el software "ampy", el cual se puede instalar directamente desde la linea de comandos como sigue:

instalacion de Pip3
```
sudo apt-get install python3-pip
```
instalacion de ampy:
```
pip3 install --user adafruit-ampy
```
una vez instalado se puede revisar el uso basico de ampy mediante el comando
```
ampy --help
```
Para ejecutar codigo desde el computador en la placa se utiliza ampy de la siguiente forma:
```
ampy -p /dev/ttyUSB0 run micodigo.py
```

ampy cuenta con un timeout, por lo cual para ejecutar bucles infinitos se debe especificar el flag -n
```
ampy -p /dev/ttyUSB0 run -n micodigo_infinito.py
```

## Instalar monitor serial Picocom
```
sudo apt-get install picocom
```
