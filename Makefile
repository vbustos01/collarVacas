export AMPY_PORT=/dev/ttyUSB0

# directorios donde se buscan los archivos
VPATH = imu/ : clases/ : sd/ : gps/ : lora/ : microfono/ : pantalla_oled/

# archivos que van en la raiz del sistema de archivos de la esp32
arch_raiz := \
main.py	\
boot.py \
imu.py	\
gps.py	\
lora.py	\
menu.py	\
mic.py	\
sd.py	

# archivos que van al directorio drivers/ de la esp32
arch_drivers := 	\
controller_esp32.py \
sx127x.py 			\
mpu6050.py 			\
constants.py 		\
cfilter.py 			\
sdcard.py 			\
ssd1306.py 			\
data_frame.py		\
cola.py				\
direccionCollar.py

# marcas de tiempo para los archivos raiz
up_raiz := $(addprefix .deploy/, $(addsuffix .dep, $(arch_raiz)))

# marcas de tiempo para los archivos de drivers/
up_drivers := $(addprefix .deploy/drivers/, $(addsuffix .dep, $(arch_drivers)))

# id por defecto del collar
id = 1

all: .deploy $(up_drivers) $(up_raiz);

.deploy/%.py.dep: %.py
	-ampy put $? > $@

.deploy/drivers/%.py.dep: %.py
	-ampy put $? drivers/$(notdir $?) > $@

# siempre se ejecuta la comprobacion de dirCollar
.deploy/drivers/direccionCollar.py.dep: comprobar_dirCollar direccionCollar.py;

.deploy:
	mkdir -p .deploy/drivers

direccionCollar.py:
	echo dirCollar = $(id) > direccionCollar.py

# comprueba la direccion del collar escrita en direccionCollar.py
comprobar_dirCollar: direccionCollar.py
ifneq ($(filter-out dirCollar =, $(shell cat direccionCollar.py)), $(id))
	echo dirCollar = $(id) > direccionCollar.py
	-ampy put direccionCollar.py drivers/direccionCollar.py > .deploy/drivers/direccionCollar.py.dep
endif

clean:
	-rm -rf .deploy/

help:
	@echo Usa make para subir solo los archivos modificados a la placa [al puerto ttyUSB0]
	@echo Usa make clean para olvidar los archivos modificados
	@echo Usa make id=2 para asignar el id numero 2 al collar [por defecto id=1]
