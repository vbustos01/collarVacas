import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
BOARD.setup()
BOARD.reset()
class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0

    def on_rx_done(self):
        #BOARD.led_on()
        #print("\nRxDone")
        paquete = self.read_payload(nocheck=True)
        direccion = int(paquete[0])
        if direccion == 0:#El paquete es para nodo central?
            comando =int(paquete[1])
            mensaje = bytes(paquete[2:]).decode()
            print("se recibio el siguiente mensaje:")
            print(mensaje)
            print(comando)
        self.clear_irq_flags(RxDone=1)
        self.var=1

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        while True:
            while (self.var==0):
                print ("Se envio: 10 0 93")
                self.write_payload([10, 0, 93]) # Send comando 
                self.set_mode(MODE.TX)
                while (self.get_irq_flags()['tx_done'] == 0):#Espera que se envie el paquete
                    pass;
                self.clear_irq_flags(TxDone=1)#Reinicio la interrupcion TxDone
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
                start_time = time.time()
                while (time.time() - start_time < 1): # wait until receive data or 10s
                    pass;
            
            self.var=0
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            time.sleep(2)

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
#print(lora.get_all_registers())
#print(lora.get_freq())
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
