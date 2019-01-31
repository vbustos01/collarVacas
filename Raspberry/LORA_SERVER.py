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
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print ("Receive: ")
        print(bytes(payload).decode("utf-8",'ignore')) # Receive DATA
        #BOARD.led_off()
        #time.sleep(2) # Wait for the client be ready
        #print ("Send: ACK")
        #self.write_payload([255, 255, 0, 0, 65, 67, 75, 0]) # Send ACK
        #self.set_mode(MODE.TX)
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
        print("modo recepcion continua")
        self.set_mode(MODE.RXCONT) # Receiver mode          
        while True:
            pass;

lora = mylora(verbose=False)
lora.set_freq(866)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py 
#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(8)
lora.set_rx_crc(True)
lora.set_lna_gain(GAIN.G1)

lora.set_preamble(8)
lora.set_implicit_header_mode(False)
#lora.set_low_data_rate_optim(True)
#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)
assert(lora.get_agc_auto_on() == 1)
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
