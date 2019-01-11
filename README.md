## Collar para la deteccion del celo y la cojera

Proyecto realizado en la universidad de la Fronteraasd

## Instalacion del firmware en la tarjeta

Para poder trabajar desde con la interfaz ESP32 el usuario debe contar con ciertos permisos para escribir sobre el puerto en el cual esta conectada la placa, en este caso ttyUSB0
```
sudo adduser MyUser dialout
sudo chmod a+rw /dev/ttyUSB0
```
NOTA: se debe modificar MyUser por el nombre de usuario respectivo.

## 