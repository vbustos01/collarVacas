export AMPY_PORT=/dev/ttyUSB0

ampy mkdir drivers

echo 'Ingrese Numero ID collar'
read var_id
echo 'dirCollar = ' ${var_id} > direccionCollar.py

#-----DRIVERS-----#

##DRIVERS IMU
ampy put acelerometro/mpu6050.py drivers/mpu6050.py
ampy put acelerometro/constants.py drivers/constants.py
ampy put acelerometro/cfilter.py drivers/cfilter.py

##DRIVERS SD
ampy put sd/sdcard.py drivers/sdcard.py

##DRIVERS PANTALLA
ampy put pantalla_oled/ssd1306.py drivers/ssd1306.py

##DRIVERS LORA
ampy put nodo_collar/all/config_lora.py drivers/config_lora.py
ampy put nodo_collar/all/controller.py drivers/controller.py
ampy put nodo_collar/all/controller_esp32.py drivers/controller_esp32.py
ampy put nodo_collar/all/sx127x.py drivers/sx127x.py

ampy put nodo_collar/all/direccionCollar.py drivers/direccionCollar.py
ampy put nodo_collar/all/data_frame.py drivers/data_frame.py



#-----MAIN y BOOT-----#
ampy put main.py
ampy put boot.py


##
#ampy put LoRa/LoRaReceiver.py
#ampy put LoRa/LoRaSender.py

