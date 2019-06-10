import os
import threading
import time
import cola
#from subirDatosServidor import *
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from data_frame import *

"""Es necesario instalar la libreria angles "pip install angles"""
BOARD.setup()#Mapeo de pines de la raspberry
BOARD.reset()#Reseteo de los pines

nodos =  1# Cantidad de Nodos Clientes(maximo 255)
t_sample= 1#Decenas de segundos(maximo 255)
INTENTOS = 3 # Cantidad de intentos para comunicarse con un Nodo cliente 
TIEMPO_CORD = TIME_SAMP*1.0/NODOS # Intervalo de tiempo para comunicarse con el Nodo cliente
SYMB_TIME_OUT = 100 # Cantidad de simbolos a esperar para detectar un preambulo


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.Recibido = False # Flag de paquete recibido
        self.TimeOut = False # Flag para detectar Timeout
        self.paqueteACK = bytes([0]) # paquete ACK utilizado para indicar la llegada de un mensaje
        self.Nodos_activos
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
            print('ERROR EN PAYLOAD')
            self.reset_ptr_rx()
            self.set_mode(MODE.RXSINGLE)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        #print("TimeOut")
        self.TimeOut = True
        self.clear_irq_flags(RxTimeout=1)
        #print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())
        #RXSINGLE

    def Enviar(self,paquete):
        self.write_payload(paquete) # Send comando 
        self.set_mode(MODE.TX)
        #tiempo_anterior = time.time()
        while (self.get_irq_flags()['tx_done'] == 0):#Espera que se envie el paquete
            pass;
        #tiempo_actual= time.time()
        #print(tiempo_actual - tiempo_anterior)
        self.clear_irq_flags(TxDone=1)#Reinicio la interrupcion TxDone  

    def start(self):
        self.set_mode(MODE.RXSINGLE)
        while True:
            if self.Recibido:
                self.Recibido=False
                if len(self.paqueteRecibidoC) == 15:
                    self.paqueteACK=[self.paqueteRecibidoC[0],nodos,t_sample]
                    self.Enviar(self.paqueteACK)
                    self.reset_ptr_rx()
                    cola1.agregar(desempaquetar(self.paqueteRecibidoC))
            #print("Ingrese Número de Nodos:")
            #os.system("clear")
def save_datLoRa(cola1):
    while cola1.vacia():
        pass;
    os.system("clear")
    print("Paquete Recibido:")
    cola1.extraer()
    
cola1=cola.cola()#creación del objeto cola1
save_data=threading.Thread(name="save_data",target=save_datLoRa,args=(1,cola1))#Creación del Hilo guardar
"""configuraciones LoRa"""
lora = mylora(verbose=False)
lora.set_freq(866)
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(8)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
lora.set_preamble(8)
lora.set_implicit_header_mode(False)
lora.set_symb_timeout(SYMB_TIME_OUT)
print(lora.__str__())
#lora.set_low_data_rate_optim(True)
#lora.set_pa_config(pa_select=1)
#assert(lora.get_agc_auto_on() == 1)
try:
    print("Server2 Iniciado...")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
