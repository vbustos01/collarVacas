import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()#Mapeo de pines de la raspberry
BOARD.reset()#Reseteo de los pines

NODOS = 20 # Cantidad de Nodos Clientes
TIME_SAMP = 60 # Tiempo de muestreo en segundos
INTENTOS = 3 # Cantidad de intentos para comunicarse con un Nodo cliente 
TIEMPO_CORD = TIME_SAMP*1.0/NODOS # Intervalo de tiempo para comunicarse con el Nodo cliente
SYMB_TIME_OUT = 200 # Cantidad de simbolos a esperar para detectar un preambulo

class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.Recibido = False # Flag de paquete recibido
        self.TimeOut = False # Flag para detectar Timeout
        self.paqueteSync = bytes([0]) # paquete de sincronización y utilizado para solicitar un dato del Nodo Cliente
        self.paqueteACK = bytes([0]) # paquete ACK utilizado para indicar la llegada de un mensaje

    def on_rx_done(self):
        paquete = self.read_payload(nocheck=True)
        if paquete:
            direccion = paquete[0]
            if direccion == 0:#El paquete es para nodo central?
                comando =paquete[1]
                if len(paquete)>2:
                    mensaje = paquete[2:]
                    mensaje = mensaje[0]<<24 | mensaje[1]<<16 | mensaje[2]<<8 | mensaje[3]
                    print("se recibio el siguiente mensaje:")
                    print(mensaje)
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
        direccionador = 0
        tiempo_anterior = 0
        while True:
            tiempo_actual = time.time()
            if ( (tiempo_actual - tiempo_anterior) >= TIEMPO_CORD):
                tiempo_anterior = tiempo_actual
            #for direccionador in range(1,NODOS+1):
                direccionador += 1
                self.TimeOut = False
                self.Recibido = False
                intentos = 0
                print ("Se envio: {0} 0 ".format(direccionador))
                self.paqueteSync = [direccionador, 0]
                self.paqueteACK = [direccionador, 1]
                self.Enviar(self.paqueteSync)
                self.reset_ptr_rx()
                self.set_mode(MODE.RXSINGLE) # Modo de recepcion de un solo paquete para uso de timeOut
                while intentos < INTENTOS:
                    if self.TimeOut:
                        print("TimeOut")
                        intentos += 1
                        self.TimeOut = False
                        self.Enviar(self.paqueteSync)#Se reenvia el paquete de sincronización
                        self.reset_ptr_rx()
                        self.set_mode(MODE.RXSINGLE)
                    if self.Recibido:
                        self.Recibido = False
                        self.Enviar(self.paqueteACK)#Se envia un ACK despues de recibir datos
                        self.reset_ptr_rx()
                        self.set_mode(MODE.RXSINGLE)
                        while not self.TimeOut:
                            if self.Recibido:
                                self.Recibido = False
                                self.Enviar(self.paqueteACK)
                                self.reset_ptr_rx()
                                self.set_mode(MODE.RXSINGLE)
                        break;
                tiempo_final = time.time()
                print(tiempo_final-tiempo_actual)
            if direccionador == NODOS :
                direccionador = 0

lora = mylora(verbose=False)
lora.set_freq(866)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py 
#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
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
#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)
#assert(lora.get_agc_auto_on() == 1)
try:
    print("START")
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
