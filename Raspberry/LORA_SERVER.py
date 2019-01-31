import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()#configura los pines
BOARD.reset()

contador = 0
PaquetesOK = 0
PaquetesPerdidos = 0
PaquetesError = 0
PaquetesRecibidos = 0
PAQUETES = 10

class mylora(LoRa):#Herada la Clase 
    global contador
    global PaquetesOK
    global PaquetesPerdidos
    global PaquetesError
    global PaquetesRecibidos

    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0

    def on_rx_done(self):

        BOARD.led_on()
        #print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        #print ("Receive: ")
        PaquetesRecibidos += 1
        mensaje=bytes(payload).decode("utf-8",'ignore')
        mensaje=mensaje[2:-1] #to discard \x00\x00 and \x00 at the end
        #print(bytes(payload).decode("utf-8",'ignore')) # Receive DATA
        if "DATA RASPBERRY PI" == mensaje:
            PaquetesOK += 1
        BOARD.led_off()
        time.sleep(0.001) # Wait for the client be ready
        #print ("Send: ACK")
        self.write_payload([255, 255, 0, 0, 65, 67, 75, 0]) # Send ACK
        self.set_mode(MODE.TX)
        self.var=1
       
       

    def on_tx_done(self):
        #print("\nTxDone")
        self.get_irq_flags()

    def on_cad_done(self):
        #print("\non_CadDone")
        self.get_irq_flags()

    def on_rx_timeout(self):
        #print("\non_RxTimeout")
        self.get_irq_flags()

    def on_valid_header(self):
        #print("\non_ValidHeader")
        self.get_irq_flags()

    def on_payload_crc_error(self):
        #print("\non_PayloadCrcError")
        PaquetesError+=1
        self.get_irq_flags()
        

    def on_fhss_change_channel(self):
        #print("\non_FhssChangeChannel")
        self.get_irq_flags()

    def start(self): 
              
        while  contador < PAQUETES:
            global PaquetesPerdidos = PAQUETES - PaquetesRecibidos
            while (self.var==0):
                print ("Send: INF")
                self.write_payload([255, 255, 0, 0, 73, 78, 70, 0]) # Send INF
                self.set_mode(MODE.TX)
                time.sleep(0.001) # there must be a better solution but sleep() works
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
            
                start_time = time.time()
                while (time.time() - start_time < 0.001): # wait until receive data or 10s
                    pass;
                self.var = 1# timeout
            
            self.var=0
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            time.sleep(0.001)
            contador += 1
            print(contador)


def program( banda , codrate , spreading):
    global BOARD
    global lora
    lora.set_bw(banda)
    lora.set_coding_rate(codrate)
    lora.set_spreading_factor(spreading)
    lora.set_rx_crc(True)
    #lora.set_lna_gain(GAIN.G1)
    #lora.set_implicit_header_mode(False)
    lora.set_low_data_rate_optim(True)
    #  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
    #lora.set_pa_config(pa_select=1)
    assert(lora.get_agc_auto_on() == 1)
    try:
        #print("START")
        lora.start()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("Exit1")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        print("Exit2")
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()

def reiniciar_contadores():
    global PaquetesOK= 0
    global PaquetesPerdidos=0
    global PaquetesError = 0
    global PaquetesRecibidos=0

lora = mylora(verbose=False)
lora.set_freq(434)
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
#LISTA_BW = [7,8,9]
#LISTA_CR = [1,2,3,4]
#LISTA_SF = [6, 8, 10, 12]
for banda in range(7 , 10 ):
    for coding in range( 1 , 5 ):
        for spread in range( 6 , 12 ):
            reiniciar_contadores()
            program(banda,coding,spread)

