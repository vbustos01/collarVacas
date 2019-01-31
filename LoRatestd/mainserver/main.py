#import LoRaDuplexCallback
#import LoRaPingPong
#import LoRaSender
#servidor Lora(Nodo Central)
from sx127x import SX127x
from controller_esp32 import ESP32Controller
import LoRaReceiver
import config_lora#Indentificador de Nodos """en este caso no se implementa"""

"""Los siguientes parametros se encuentran por defecto para configurarlos modifique el diccionario parametros despues de este ejemplo(por defecto)"""
# parameters = {'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,
#                                'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
#                                'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}
"""La estos parametros deben ser iguales Entre Esclavo y Maestro a continuación se muestran los rangos disponibles(pensado en modulo sx1276)"""
# BW (7.8E3, 10.4E3, 15.6E3, 20.8E3, 31.25E3, 41.7E3, 62.5E3, 125E3, 250E3)
# spreading_factor (6 to 12)
# coding_rate (5 to 8)
"""IMPORTANTE REVIZAR Payload pag 31 data sx127x """
 #parametros = {'frequency': 869E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}
objeto=SX127x(name = 'LoRa1',parameters = {'frequency': 866E6, 'tx_power_level': 14, 'signal_bandwidth': 125E3,'spreading_factor': 10, 'coding_rate':5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC':True})
controller = ESP32Controller()#Configuracion de Pines y SPI para modificarlos realizarlo en 
                                    #En esta seccion ocurre una herencia multiple del objeto lora
lora = controller.add_transceiver(objeto,
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0) 
                                
#  # Transceiver permite agregar numero del pin chip SELECT y  pines de interrupciones para mas funciones del Modulo LoRa
#      def add_transceiver(self,
#                         transceiver,
#                         pin_id_ss = PIN_ID_FOR_LORA_SS,
#                         pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
#                         pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
#                         pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
#                         pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
#                         pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
#                         pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5):

LoRaReceiver.receive(lora)
