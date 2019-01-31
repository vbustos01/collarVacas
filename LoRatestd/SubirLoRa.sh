#!/bin/bash
echo 'Ingrese opcion'
echo '1.-Modo Emisor'
echo '2.-Modo Receptor'
read var1
#cd mainclient | sudo ampy -p /dev/ttyUSB0 put main.py

case $var1 in
	1)
		echo 'Ingrese Puerto'
		echo '0.-/dev/ttyUSB0'
		echo '1.-/dev/ttyUSB1'
		echo '2.-/dev/ttyUSB2'
		echo '3.-/dev/ttyUSB3'
		read var2
		cd mainclient
		sudo ampy -p /dev/ttyUSB${var2} put main.py
		echo 'client subido ...'
		cd ..
		sudo ampy -p /dev/ttyUSB${var2} put all/LoRaSender.py
		echo 'LoRaSender subido ...'
		;;
	2)
		echo 'Ingrese Puerto'
		echo '0.-/dev/ttyUSB0'
		echo '1.-/dev/ttyUSB1'
		echo '2.-/dev/ttyUSB2'
		echo '3.-/dev/ttyUSB3'
		read var2
		cd mainserver
		sudo ampy -p /dev/ttyUSB${var2} put main.py
		echo 'server subido ...'
		cd ..
		sudo ampy -p /dev/ttyUSB${var2} put all/LoRaReceiver.py
		echo 'LoRaReciver subido ...'
		;;
	*)
		echo "Opcion Desconocida!"
		exit 1
		;;
esac

sudo ampy -p /dev/ttyUSB${var2} put all/config_lora.py
echo 'config_lora subido ...'
sudo ampy -p /dev/ttyUSB${var2} put all/controller.py
echo 'controller subido ...'
sudo ampy -p /dev/ttyUSB${var2} put all/controller_esp32.py
echo 'controller_esp32 subido ...'
sudo ampy -p /dev/ttyUSB${var2} put all/sx127x.py
echo 'sx127x subido ...'
sudo ampy -p /dev/ttyUSB${var2} put all/ssd1306.py
echo 'Pantalla_i2c subido ...'
sudo ampy -p /dev/ttyUSB${var2} put all/direccionCollar.py
echo 'Direccion de collar subida ...'
