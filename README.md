## Instalacion del firmware en la tarjeta ESP32

La guía paso a paso se encuentra en la siguiente url (en inglés): 
https://github.com/micropython/micropython/blob/master/ports/esp32/README.md

Se debe descargar el repositorio de la versión de micropython que contiene la implementación la interfaz I2S necesaria para el funcionamiento del micrófono.
https://github.com/miketeachman/micropython/tree/esp32-i2s

Luego de seguir los pasos se tendrán los siguientes directorios:

  ![setup](https://i.imgur.com/dzFEmQF.png)
  
Finalmente, como se muestra en la guia, se compila la build de micropython y se sube al microcontrolador.
```
$ cd micropython/ports/esp32
$ make
...
$ make erase
...
$ make deploy
```

## Instalar monitor serial Picocom
```
$ sudo apt-get install picocom
```
