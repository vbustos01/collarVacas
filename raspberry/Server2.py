#!/usr/bin/env python3
import os
import threading
import time
import cola
from subirDatosServidor import *
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from data_frame import *
import pickle
from angles import sexa2deci

"""Es necesario instalar la libreria angles "pip install angles"""
BOARD.setup()#Mapeo de pines de la raspberry
BOARD.reset()#Reseteo de los pines
debug = True
def debugmsg(msg):
    if debug:
        print("[debug] : "+str(msg))
nodos =  1# Cantidad de Nodos Clientes(maximo 255)
t_sample= 1#Decenas de segundos(maximo 255)

class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.Recibido = False # Flag de paquete recibido
        self.TimeOut = False # Flag para detectar Timeout
        self.paqueteACK = bytes([0]) # paquete ACK utilizado para indicar la llegada de un mensaje
        self.paqueteRecibidoC=bytes(0)
    #Callbacks
    def on_rx_done(self):
        paquete = self.read_payload(nocheck=True)
        if paquete:
            #direccion = paquete[0]
        #if direccion == 0:#El paquete es para nodo central?
            #comando =paquete[1]
            if len(paquete)>5:
                self.paqueteRecibidoC=paquete
                self.RSSI = self.get_pkt_rssi_value() #RSSI(dBm) del paquete recibido
                #mensaje = paquete[2:]
                #mensaje = mensaje[0]<<24 | mensaje[1]<<16 | mensaje[2]<<8 | mensaje[3]
                #print("se recibio el siguiente mensaje:")
                #print(mensaje)
            self.Recibido = True
            self.clear_irq_flags(RxDone=1)
        else:
            self.clear_irq_flags(RxDone=1)
            self.clear_irq_flags(PayloadCrcError=1)
            self.Recibido = False
            debugmsg('ERROR EN PAYLOAD')
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        debugmsg("TxDone")
        debugmsg(self.get_irq_flags())

    def on_cad_done(self):
        debugmsg("\non_CadDone")
        debugmsg(self.get_irq_flags())

    def on_rx_timeout(self):
        debugmsg("TimeOut")
        self.TimeOut = True
        self.clear_irq_flags(RxTimeout=1)
        #print(self.get_irq_flags())

    def on_valid_header(self):
        debugmsg("\non_ValidHeader")
        debugmsg(self.get_irq_flags())

    def on_payload_crc_error(self):
        debugmsg("\non_PayloadCrcError")
        debugmsg(self.get_irq_flags())

    def on_fhss_change_channel(self):
        debugmsg("\non_FhssChangeChannel")
        print(self.get_irq_flags())
        #RXSINGLE

    def Enviar(self,paquete):
        self.write_payload(paquete) # Se escribe el payload en fifo
        self.set_mode(MODE.TX)
        #tiempo_anterior = time.time()
        while (self.get_irq_flags()['tx_done'] == 0):#Espera que se envie el paquete
            pass;
        #tiempo_actual= time.time()
        #print(tiempo_actual - tiempo_anterior)
        self.clear_irq_flags(TxDone=1)#Reinicio la interrupcion TxDone  

    def start(self):
        self.set_mode(MODE.RXCONT)
        while True:
            if self.Recibido:
                self.Recibido=False
                if len(self.paqueteRecibidoC) == 15:
                    self.paqueteACK=[self.paqueteRecibidoC[0],0]
                    self.Enviar(self.paqueteACK)
                    self.reset_ptr_rx()
                    cola1.agregar([self.paqueteRecibidoC,self.RSSI])
                    self.set_mode(MODE.RXCONT)
            #print("Ingrese Número de Nodos:")
            #os.system("clear")
def save_datLoRa():
    contador=0
    global cola1
    global stop_th
    while True:
        while cola1.vacia():
            if stop_th:
                break      
        if stop_th:
            break
        #os.system("clear")
        data = cola1.extraer()       
        dato=desempaquetar(data[0])#Desempaquetado y extracción de la cola
        Latitud=sexa2deci(dato['location'][0],dato['location'][1],dato['location'][2],0)
        Longitud=sexa2deci(dato['location'][3],dato['location'][4],dato['location'][5],0)
        try:
            pickle.dump({'Latitud':Latitud,'Longitud':Longitud},open("/home/pi/datos/vaca_ID{}.dat".format(dato['address']),'wb'),protocol=2)
        except:
            debugmsg("Error al guardar en .dat")
        try:
            subirdatosVacas(dato)
            print(dato)
            print("RSSI : {}[dBm]".format(data[1]))
        except:
            debugmsg("Error al subir en Servidor")
        contador += 1
        print("Server2 Iniciado")
        print("Radio LoRa encendida")
        print("{} Paquetes Recibidos".format(contador))

stop_th=False
cola1=cola.cola()#creación del objeto cola1
save_data=threading.Thread(target=save_datLoRa)#Creación del Hilo guardar
save_data.start()
"""configuraciones LoRa"""
lora = mylora(verbose=False)
lora.set_freq(866)
lora.set_pa_config(pa_select=1, max_power=15, output_power=15)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(8)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
lora.set_preamble(8)
lora.set_implicit_header_mode(False)
#lora.set_symb_timeout(SYMB_TIME_OUT)
debugmsg(lora.__str__())
#time.sleep(2)
#lora.set_low_data_rate_optim(True)
#lora.set_pa_config(pa_select=1)
#assert(lora.get_agc_auto_on() == 1)
try:
    print("Server2 Iniciado")
    print("Radio LoRa encendida")
    lora.start()
except KeyboardInterrupt:
    stop_th=True
    save_data.join()
    sys.stdout.flush()
    print("Server2 Finalizado")
    sys.stderr.write("Por interrupción de teclado\n")
finally:
    sys.stdout.flush()
    print("Radio Lora modo Sleep")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
