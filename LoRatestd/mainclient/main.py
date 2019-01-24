#import LoRaDuplexCallback
#import LoRaPingPong
import LoRaSender
import LoRaReceiver
import config_lora
from sx127x import SX127x
from controller_esp32 import ESP32Controller


#{'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False}

controller = ESP32Controller()
objeto=SX127x(name = 'LoRa1',parameters = {'frequency': 866E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False})
lora = controller.add_transceiver(objeto,
                                  pin_id_ss = ESP32Controller.PIN_ID_FOR_LORA_SS,
                                  pin_id_RxDone = ESP32Controller.PIN_ID_FOR_LORA_DIO0)

#LoRaDuplexCallback.duplexCallback(lora)
#LoRaPingPong.ping_pong(lora)
LoRaSender.send(lora)
#LoRaReceiver.receive(lora)
