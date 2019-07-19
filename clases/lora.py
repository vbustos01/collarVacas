
###########################################################################################################
#################INTRUCCIONES##############################################################################
#   1. Para utilizar esta clase se debe importar en el main.py de tal forma que se puede aprovechar       #
#   el hilo "LoRa_thread()" el cual se encarga de transmitir datos en cola a travez de lora, para         #
#   importarlo se recomienda "import lora".                                                               #
#   2. Para agregar paquetes a la cola se debe crear un diccionario (pre_frame) el cual debe tener las    #
#   caracteristicas descritas en el driver "data_frame.py" (collarVacas/nodo_collar/data_frame.py).       #
#   3. El preframe creado se agrega a la cola como:                                                       #
#   lora.lora_th.addMsn2cola(pre_frame)                                                                   #
#   4. De esta forma se agregan mensajes a la cola los cuales se empaquetan y se transmiten por LoRa.     #
###########################################################################################################
 
import _thread
import time
from drivers.cola import cola 
from drivers.data_frame import *
import drivers.config_lora
from drivers.sx127x import SX127x
from drivers.controller_esp32 import ESP32Controller
from drivers.direccionCollar import dirCollar
#{'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}

class LoRa:

    def __init__(self,
                 name = 'SX127x',
                 parameters = {'frequency': 866,'Pa_Config':{"pa_select":0,"max_power":7,"output_power":10}, 'signal_bandwidth': 125E3,
                               'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
                               'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True},
                 intentosACK=2,
                 time_out_Symb = 200):
        controller = ESP32Controller()#llamado a mapeo de pines ESP32
        objeto=SX127x(name,parameters)
        self.lora = controller.add_transceiver(objeto,
                                          pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                          pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0,
                                          pin_id_RxTimeout= ESP32Controller.PIN_ID_FOR_LORA_DIO1)
        self.paqueteEnviar = bytearray()
        self.paqueteActual = bytearray()
        self.intentosACK = intentosACK
        self.intentos= 0 #intentos actuales para reenviar paquetes
        self.detectACK = True
        self.SYMB_TIME_OUT = time_out_Symb
        self.MapPinCAD=False #[False=>DI0:RxDone,DI1:TimeOut,True=DIO:CAD]
        global colamsn

    def beginIRQ(self):
        #print("LoRa Collar")
        self.lora.onReceive(self.on_receive)#Asigna una función para la interrupcion del pin DIO0
        self.lora.onTimeout(self.on_timeout, self.SYMB_TIME_OUT)#Asigna una función para la interrupcion del pin DIO1 y asigna un Timeout
        # sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}          
        # pre_frame ={'address':255,'cmd':7,                                
        #             'sensors':sensors,'location':"3844.7556,S,07236.9213,W", 
        #             't_unix':454545666,'bateria':1024,'C_close':True}
        self.setModoSTBY()
        #self.paqueteActual = empaquetar(pre_frame)

    def CAD_Done(self):
        pass
    def CAD_Detected(self):
        pass
    def Rx_Done(self, paquete):
        pass
    def Rx_TimeOut(self):
        pass

    def on_receive(self,paquete):
        if paquete:
            direccion = paquete[0]
            if direccion == dirCollar: 
                print("Recibi:")
                if paquete[1] == 0:
                    self.detectACK = True#llego un paquete ACK
                    print("ACK")
                    self.intentos= 0
            else:
                print("Direccion Diferente")
                self.reenviar()
        else :
            print("Paquete con Error")
            self.reenviar()
        print("RSSI:{0}".format(self.lora.packetRssi()))

    def reenviar(self):
        self.intentos += 1
        if self.intentos <= self.intentosACK:
            if not(self.detectACK):
                self.lora.bytesprintln(self.paqueteEnviar)
                self.setModoSingle()#se espera nuevamente un ACK
        else:
            print("True ACK detect")
            self.detectACK = True#intentos no cumplidos
            self.intentos = 0

    def on_timeout(self):
        #print("TimeOut!")
        self.intentos += 1
        if self.intentos <= self.intentosACK:
            if not(self.detectACK):
                self.lora.bytesprintln(self.paqueteEnviar)
                self.setModoSingle()#se espera nuevamente un ACK
        else:
            print("True ACK detect")
            self.detectACK = True#intentos no cumplidos
            self.intentos = 0

    def addMsn2cola(self,preframe):
        colamsn.agregar(empaquetar(preframe))
    
    def setModoContinuoRx(self):
        self.lora.receive()

    def setModoSingle(self):
        self.lora.receiveSingle()
    
    def setModoSleep(self):
        self.lora.sleep()

    def setModoSTBY(self):
        self.lora.standby()

    def setModoCAD(self):
        self.lora.CAD()

def LoRa_thread():
    global colamsn
    global lora_th
    set_sleep = False
    print("Radio Lora Iniciada\n")
    while True:
        while not(lora_th.detectACK):#no se enviara otro paquete hasta que se confirme un ACK en n intentos
            time.sleep(0.4)
        while colamsn.vacia():#Función bloqueante, Espera algun elemento en la cola
            if not(set_sleep):#Si no esta en modo sleep
                lora_th.setModoSleep()
                set_sleep=True
                #print("sleep")
            time.sleep(5)
        print("extraccion")
        lora_th.detectACK=False#se reinicia el ACK
        set_sleep=False#Se cambio de modo
        #automaticamente se pasa a STBY con bytesprintln
        lora_th.paqueteEnviar=colamsn.extraer()
        lora_th.lora.bytesprintln(lora_th.paqueteEnviar)
        lora_th.setModoSingle()#Se espera por un ACK
        

colamsn=cola()
lora_th=LoRa()
print(lora_th.lora.read_all_regs())
lora_th.beginIRQ()
_thread.start_new_thread(LoRa_thread,())
