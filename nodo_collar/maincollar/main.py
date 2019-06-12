import Clientecollar as LoRa
import _thread
import cola
import data_frame
LoRa.LoRa()

def LoRa_thread(cola,lora,no_sleep=True):

    while cola.vacia():
        if no_sleep:
            lora.setModoSleep()
            no_sleep=False
        pass;
    lora.setModoSTBY()
    
    