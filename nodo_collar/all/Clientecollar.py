from direccionCollar import *
from time import time
from data_frame import *
import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller

#{'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}

class LoRa:

    def __init__(self,
                 name = 'SX127x',
                 parameters = {'frequency': 866E6, 'tx_power_level': 17, 'signal_bandwidth': 125E3,
                               'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
                               'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True},
                 intentosACK=2,
                 time_out_Symb = 200):
        print("init LoRa")
        controller = ESP32Controller()#llamado a mapeo de pines ESP32
        objeto=SX127x(name,parameters)
        self.lora = controller.add_transceiver(objeto,
                                          pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                          pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0,
                                          pin_id_RxTimeout= ESP32Controller.PIN_ID_FOR_LORA_DIO1)
        self.paqueteEnviar = bytearray()
        self.paqueteActual = bytearray()
        self.direccionCollar=dirCollar
        self.intentosACK = intentosACK
        self.intentos = 0
        self.paqueteSync = False
        self.simbolos_Time_Out = time_out_Symb

    def beginIRQ(self):
        print("interrupciones activas")
        self.lora.onReceive(self.on_receive)#Asigna una función para la interrupcion del pin DIO0
        self.lora.onTimeout(self.on_timeout,self.simbolos_Time_Out)#Asigna una función para la interrupcion del pin DIO1 y asigna un Timeout
        # sensors = {'GPS':True,'IMU':False,'SD':True,'MIC':False}          
        # pre_frame ={'address':255,'cmd':7,                                
        #             'sensors':sensors,'location':"3844.7556,S,07236.9213,W", 
        #             't_unix':454545666,'bateria':1024,'C_close':True}
        self.lora.sleep()#modo sleep


    def on_receive(self,paquete):
        if paquete: 
            if paquete[0] == self.direccionCollar:
                comando = paquete[1]
                print("Paquete recibido:")
                if comando == 0:
                    self.paqueteSync = True#llego un paquete de sincronización
                    self.lora.bytesprintln(self.paqueteActual)
                    self.paqueteEnviar = self.paqueteActual
                    print("Sync")
                    self.lora.receiveSingle()#necesario ya que despues de un envio la radio cambia a mod sleep
                elif self.paqueteSync and (comando == 1):
                    self.paqueteSync = False#llego un paquete ACK
                    print("ACK")
                    self.intentos = 0
                    self.lora.receive()
            else:
                print("Direccion no corresponde")
        else :
            print("Paquete con Error")
            self.lora.receive()
        if self.paqueteSync:
            self.lora.receiveSingle()
        print("RSSI:{0}".format(self.lora.packetRssi()))
    
    def on_timeout(self):
        self.intentos += 1
        if self.intentos <= self.intentosACK:
            if self.paqueteSync:
                self.lora.bytesprintln(self.paqueteEnviar)
                self.lora.receiveSingle()#se espera nuevamente un ACK
        else:
            self.lora.receive()#intentos no cumplidos
    
    def setMsn(self,preframe):
        self.paqueteActual=empaquetar(preframe)
    
    def setModoContinuoRx(self):
        self.lora.receive()

    def setModoSingle(self):
        self.lora.receiveSingle()
    
    def setModoSleep(self):
        self.lora.sleep()

    def setModoSTBY(self):
        self.lora.standby()

        
