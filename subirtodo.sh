export AMPY_PORT=/dev/ttyUSB0

ampy mkdir drivers


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
ampy put lora/config_lora.py drivers/config_lora.py
ampy put lora/controller.py drivers/controller.py
ampy put lora/controller_esp32.py drivers/controller_esp32.py
ampy put lora/sx127x.py drivers/sx127x.py

#-----MAIN y BOOT-----#
ampy put main.py
ampy put boot.py


##
#ampy put LoRa/LoRaReceiver.py
#ampy put LoRa/LoRaSender.py

