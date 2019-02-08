#!/bin/bash
echo 'Script para subir modulos micropython a Esp32'
echo 'Ingrese la opcion del puerto en donde se encuentra el dispositivo'
#cd mainclient | sudo ampy -p /dev/ttyUSB0 put main.py
echo '0.-/dev/ttyUSB0'
echo '1.-/dev/ttyUSB1'
echo '2.-/dev/ttyUSB2'
echo '3.-/dev/ttyUSB3'
read var2
cd maincollar
sudo ampy -p /dev/ttyUSB${var2} put main.py
echo 'main subido ...'
cd ..
sudo ampy -p /dev/ttyUSB${var2} put all/Clientecollar.py
echo 'Clientecollar subido ...'
echo 'Ingrese Numero ID collar'
read var3
echo 'dirCollar = '${var3} > all/direccionCollar.py
sudo ampy -p /dev/ttyUSB${var2} put all/direccionCollar.py
echo 'Direccion de collar subida ...'
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
sudo ampy -p /dev/ttyUSB${var2} put all/data_frame.py
echo 'Pantalla_i2c subido ...'
