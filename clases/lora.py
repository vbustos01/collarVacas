import _thread
import time
from drivers.cola import cola 
from drivers.direccionCollar import *
from drivers.data_frame import *
import drivers.config_lora
from drivers.sx127x import SX127x
from drivers.controller_esp32 import ESP32Controller

#{'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}

class LoRa:

    def __init__(self,
                 name = 'SX127x',
                 parameters = {'frequency': 866E6, 'tx_power_level': 10, 'signal_bandwidth': 125E3,
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
    print("se inicio el hilo")
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
lora_th.beginIRQ()
_thread.start_new_thread(LoRa_thread,())
