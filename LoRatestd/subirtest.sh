#!/bin/bash
echo 'ingrese modo emisor o receptor'
read var1
echo $var1

#cd mainclient | sudo ampy -p /dev/ttyUSB0 put main.py

case $var1 in
	emisor)
		echo 'entre en emisor'
		cd mainclient
		sudo ampy -p /dev/ttyUSB0 put main.py
		;;
	receptor)
		cd mainserver
		sudo ampy -p /dev/ttyUSB0 put main.py
		;;
	*)
		echo "ingrese correctamente"
		;;
esac

cd ..
ampy -p /dev/ttyUSB0 put config_lora.py
ampy -p /dev/ttyUSB0 put controller.py
ampy -p /dev/ttyUSB0 put controller_esp32.py
ampy -p /dev/ttyUSB0 put sx127x.py
ampy -p /dev/ttyUSB0 put LoRaReceiver.py
ampy -p /dev/ttyUSB0 put LoRaSender.py


