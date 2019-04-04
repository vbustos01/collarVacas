"""
MODULO QUE IMPLEMENTA LA FUNCION DE INGRESO DE TEXTO POR PICOCOM
CON UN TIMEOUT.
PERMITE DEBUGEAR EN TERRENO DE FORMA MAS SENCILLA MEDIANTE EL USO
DE UN MENU. Y EN CASO DE NO EXISTIR NECESIDAD DE DEBUGEAR, EL 
PROGRAMA SEGUIRA SU CURSO LUEGO DEL TIMEOUT.
(precaucion: este metodo hace un hard reset a la placa)
"""
from machine import Timer, reset

FILENAME = "timeout_state.config" #nombre del archivo de configuracion
TIMEOUT = 3000 #(ms)
reading=None

"""
Este metodo se llama cuando no se presiona ninguna 
tecla antes de TIMEOUT/1000 segundos.
Guarda un flag de este suceso en la flash y se reinicia la placa.
"""
def inputtimeout():
	if reading == None:
		f = open(FILENAME, "wb")
		f.write(b'1')
		f.close()
		reset()

"""
Se comporta igual a input(), si la placa se inicia con el flag=1
salta y devuelve None, en caso contrario retorna el texto ingresado
por el usuario.
"""
def inputread():
	if getlasttimeoutstate()==b'0':
		timer = Timer(-1)
		timer.init(period=TIMEOUT, mode=Timer.ONE_SHOT, callback=lambda t:inputtimeout())
		reading = input()
	else:
		reading=None
	return reading

"""
Carga el ultimo estado del flag guardado en la flash.
Finalmente devuelve el flag a 0 en la flash para que vuelva
al estado inicial en el proximo inicio.
"""
def getlasttimeoutstate():
	state = b'0'
	try:
		f = open(FILENAME, "rb+")
		state = f.read()
		f.close()
	except OSError:
		print("estado no encontrado, creando archivo...")
	
	resettimeout();

	return state

"""
Reinicia/crea el archivo de configuracion con el flag=0.
"""
def resettimeout():
	f = open(FILENAME, "wb")
	f.write(b'0')
	f.close()
