# inicializacion antena lora
#import Clientecollar, config_lora
#from sx127x import SX127x
#from controller_esp32 import ESP32Controller as controller
import inputwithtimeout as iwt

text=iwt.inputread()


if text != None:
	print("se escribio: "+text)
	#  
else:
	pass
	# aqui va el codigo principal que se ejecuta en caso de haber ocurrido el timeout

#{'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}
"""
objeto=SX127x(name = 'LoRa1',parameters = {'frequency': 866E6, 'tx_power_level': 17 , 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': True})

lora = controller.add_transceiver(objeto,
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0,
                                  pin_id_RxTimeout= ESP32Controller.PIN_ID_FOR_LORA_DIO1)
Clientecollar.collar(lora)
"""