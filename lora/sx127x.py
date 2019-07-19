from time import sleep
import gc
import sys

PA_OUTPUT_RFO_PIN = 0
PA_OUTPUT_PA_BOOST_PIN = 1

# registers
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FRF_MSB = 0x06
REG_FRF_MID = 0x07
REG_FRF_LSB = 0x08
REG_PA_CONFIG = 0x09
REG_OCP = 0x0b
REG_LNA = 0x0c
REG_FIFO_ADDR_PTR = 0x0d

REG_FIFO_TX_BASE_ADDR = 0x0e
FifoTxBaseAddr = 0x00
# FifoTxBaseAddr = 0x80

REG_FIFO_RX_BASE_ADDR = 0x0f
FifoRxBaseAddr = 0x00
REG_FIFO_RX_CURRENT_ADDR = 0x10
REG_IRQ_FLAGS_MASK = 0x11
REG_IRQ_FLAGS = 0x12
REG_RX_NB_BYTES = 0x13
REG_PKT_RSSI_VALUE = 0x1a
REG_PKT_SNR_VALUE = 0x1b
REG_MODEM_CONFIG_1 = 0x1d
REG_MODEM_CONFIG_2 = 0x1e
REG_SYMB_TIMEOUTLSB = 0x1f 
REG_PREAMBLE_MSB = 0x20
REG_PREAMBLE_LSB = 0x21
REG_PAYLOAD_LENGTH = 0x22
REG_FIFO_RX_BYTE_ADDR = 0x25
REG_MODEM_CONFIG_3 = 0x26
REG_RSSI_WIDEBAND = 0x2c
REG_DETECTION_OPTIMIZE = 0x31
REG_DETECTION_THRESHOLD = 0x37
REG_SYNC_WORD = 0x39
REG_DIO_MAPPING_1 = 0x40
REG_VERSION = 0x42

# modes
MODE_LONG_RANGE_MODE = 0x80  # bit 7: 1 => LoRa mode
MODE_SLEEP = 0x00
MODE_STDBY = 0x01
MODE_TX = 0x03
MODE_RX_CONTINUOUS = 0x05
MODE_RX_SINGLE = 0x06
MODE_CAD = 0x07

# PA config
PA_BOOST = 0x80

# IRQ masks
IRQ_TX_DONE_MASK = 0x08
IRQ_PAYLOAD_CRC_ERROR_MASK = 0x20
IRQ_VALID_HEAD_MASK = 0x10
IRQ_RX_DONE_MASK = 0x40
IRQ_RX_TIME_OUT_MASK = 0x80
IRQ_CAD_DONE = 0x04
IRQ_CAD_DETECTED = 0x01
IRQ_FHSS_CHANGE_CHANNEL = 0x02

# Buffer size
MAX_PKT_LENGTH = 255


class SX127x:
    
    def __init__(self,
                 name = 'SX127x',
                 parameters = {'frequency': 866, 'Pa_Config':{'pa_select':0,'max_power':7,'output_power':10}, 'signal_bandwidth': 125E3,
                               'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
                               'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False},
                 onReceive = None):

        self.name = name
        self.parameters = parameters
        self.CAD_ON = False #Se realiza un cálculo de actividad del canal
        self._onReceive = onReceive
        self._onTimeout = None
        self._lock = False

    def init(self, parameters = None):
        if parameters: self.parameters = parameters
        init_try = True
        re_try = 0
        # check version
        while(init_try and re_try < 10):
            version = self.readRegister(REG_VERSION)
            re_try = re_try + 1
            if(version == 0x12):
                init_try = False
        if version != 0x12:
            raise Exception('Invalid version.')
        # put in LoRa and sleep mode
        self.sleep()

        # config
        self.setFreqMhz(self.parameters['frequency'])
        self.setSignalBandwidth(self.parameters['signal_bandwidth'])

        # set LNA boost
        self.writeRegister(REG_LNA, self.readRegister(REG_LNA) | 0x03)

        # set auto AGC
        self.writeRegister(REG_MODEM_CONFIG_3, 0x04)

        self.set_pa_config(self.parameters['Pa_Config'])#se descomprime el diccionario Pa_Config para obtener cada parametro 
        self._implicitHeaderMode = None
        self.implicitHeaderMode(self.parameters['implicitHeader'])
        self.setSpreadingFactor(self.parameters['spreading_factor'])
        self.setCodingRate(self.parameters['coding_rate'])
        self.setPreambleLength(self.parameters['preamble_length'])
        self.setSyncWord(self.parameters['sync_word'])
        self.enableCRC(self.parameters['enable_CRC'])

        # set LowDataRateOptimize flag if symbol time > 16ms (default disable on reset)
        # self.writeRegister(REG_MODEM_CONFIG_3, self.readRegister(REG_MODEM_CONFIG_3) & 0xF7)  # default disable on reset
        if 1000 / (self.parameters['signal_bandwidth'] / 2**self.parameters['spreading_factor']) > 16:
            self.writeRegister(REG_MODEM_CONFIG_3, self.readRegister(REG_MODEM_CONFIG_3) | 0x08)

        # set base addresses
        self.writeRegister(REG_FIFO_TX_BASE_ADDR, FifoTxBaseAddr)
        self.writeRegister(REG_FIFO_RX_BASE_ADDR, FifoRxBaseAddr)

        self.standby()

    def beginPacket(self, implicitHeaderMode = False):
        self.standby()
        self.implicitHeaderMode(implicitHeaderMode)

        # reset FIFO address and paload length
        self.writeRegister(REG_FIFO_ADDR_PTR, FifoTxBaseAddr)
        self.writeRegister(REG_PAYLOAD_LENGTH, 0)

    def endPacket(self):
        # put in TX mode
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_TX)

        # wait for TX done, standby automatically on TX_DONE
        while (self.readRegister(REG_IRQ_FLAGS) & IRQ_TX_DONE_MASK) == 0:
            pass

        # clear IRQ's
        self.writeRegister(REG_IRQ_FLAGS, IRQ_TX_DONE_MASK)

        self.collect_garbage()

    def write(self, buffer):
        currentLength = self.readRegister(REG_PAYLOAD_LENGTH)
        size = len(buffer)

        # check size
        size = min(size, (MAX_PKT_LENGTH - FifoTxBaseAddr - currentLength))

        # write data
        for i in range(size):
            self.writeRegister(REG_FIFO, buffer[i])

        # update length
        self.writeRegister(REG_PAYLOAD_LENGTH, currentLength + size)
        return size

    def aquire_lock(self, lock = False):
        self._lock = False

    def println(self, string, implicitHeader = False):
        self.aquire_lock(True)  # wait until RX_Done, lock and begin writing.
        self.beginPacket(implicitHeader)
        self.write(string.encode())
        self.endPacket()
        self.aquire_lock(False) # unlock when done writing

    def bytesprintln(self, bytesdata, implicitHeader = False):
        self.aquire_lock(True)  # wait until RX_Done, lock and begin writing.
        self.beginPacket(implicitHeader)
        self.write(bytesdata)
        self.endPacket()
        self.aquire_lock(False) # unlock when done writing

    def getIrqFlags(self):#En esta funcion los flags de los registros son reiniciados.
        irqFlags = self.readRegister(REG_IRQ_FLAGS)
        self.writeRegister(REG_IRQ_FLAGS, irqFlags)
        return irqFlags

    def get_irq_flags_mask(self):
        v = self.readRegister(0x11)
        return dict(
                rx_timeout     = v >> 7 & 0x1,
                rx_done        = v >> 6 & 0x1,
                crc_error      = v >> 5 & 0x1,
                valid_header   = v >> 4 & 0x1,
                tx_done        = v >> 3 & 0x1,
                cad_done       = v >> 2 & 0x1,
                fhss_change_ch = v >> 1 & 0x1,
                cad_detected   = v >> 0 & 0x1,
            )

    def packetRssi(self):
        return (self.readRegister(REG_PKT_RSSI_VALUE) - (164 if self._frequency < 862 else 157)) 

    def packetSnr(self):
        return (self.readRegister(REG_PKT_SNR_VALUE)) * 0.25

    def standby(self):
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_STDBY)
    
    def CAD(self):
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_CAD)

    def sleep(self):
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_SLEEP)

    def readCRCmsg(self):
        return ( self.readRegister(REG_IRQ_FLAGS) & 0x20 )

    def readIRQFLAGS(self):
        return (self.readRegister(REG_IRQ_FLAGS))

    def readpowertx(self):
        return self.readRegister(REG_PA_CONFIG)

    def get_pa_config(self, convert_dBm=False):
        v = self.readRegister(REG_PA_CONFIG)
        pa_select    = v >> 7 
        max_power    = v >> 4 & 0b111
        output_power = v & 0b1111
        if convert_dBm:
            if pa_select:
                max_power = max_power * .6 + 10.8
                output_power = 17 - (15 - output_power)
            else:
                max_power = max_power * .6 + 10.8
                output_power = max_power - (15 - output_power)
        return dict(
                pa_select    = pa_select,
                max_power    = max_power,
                output_power = output_power
            )
    
    def set_pa_config(self,pa_configs):
        current = self.get_pa_config()
        pa_configs = {s: current[s] if pa_configs[s] is None else pa_configs[s] for s in pa_configs}
        val = (pa_configs['pa_select'] << 7) | (pa_configs['max_power'] << 4) | (pa_configs['output_power'])
        self.writeRegister(REG_PA_CONFIG,val)

    def setFreqMhz(self, freq):#freq. en MHz
        freq =137 if freq < 137 else (1020 if freq > 1020 else freq) # limites para los chips SX127(6-7)
        self._frequency = freq
        freq = int(freq*16384)

        msb = (freq >> 16) & 0xFF # 8 bits más significativos 
        midsb = (freq >> 8) & 0xFF # 8 bits centrales
        lsb = freq & 0xFF # 8 bits menos significativos

        self.writeRegister(REG_FRF_MSB, msb)
        self.writeRegister(REG_FRF_MID, midsb)
        self.writeRegister(REG_FRF_LSB, lsb)

    def setSpreadingFactor(self, sf):
        sf = min(max(sf, 6), 12)
        self.writeRegister(REG_DETECTION_OPTIMIZE, 0xc5 if sf == 6 else 0xc3)
        self.writeRegister(REG_DETECTION_THRESHOLD, 0x0c if sf == 6 else 0x0a)
        self.writeRegister(REG_MODEM_CONFIG_2, (self.readRegister(REG_MODEM_CONFIG_2) & 0x0f) | ((sf << 4) & 0xf0))

    def setSignalBandwidth(self, sbw):
        bins = (7.8E3, 10.4E3, 15.6E3, 20.8E3, 31.25E3, 41.7E3, 62.5E3, 125E3, 250E3)

        bw = 9
        for i in range(len(bins)):
            if sbw <= bins[i]:
                bw = i
                break

        # bw = bins.index(sbw)

        self.writeRegister(REG_MODEM_CONFIG_1, (self.readRegister(REG_MODEM_CONFIG_1) & 0x0f) | (bw << 4))

    def setCodingRate(self, denominator):
        denominator = min(max(denominator, 5), 8)
        cr = denominator - 4
        self.writeRegister(REG_MODEM_CONFIG_1, (self.readRegister(REG_MODEM_CONFIG_1) & 0xf1) | (cr << 1))

    def setPreambleLength(self, length):
        self.writeRegister(REG_PREAMBLE_MSB,  (length >> 8) & 0xff)
        self.writeRegister(REG_PREAMBLE_LSB,  (length >> 0) & 0xff)

    def enableCRC(self, enable_CRC = False):
        modem_config_2 = self.readRegister(REG_MODEM_CONFIG_2)
        config = modem_config_2 | 0x04 if enable_CRC else modem_config_2 & 0xfb
        self.writeRegister(REG_MODEM_CONFIG_2, config) #

    def setSyncWord(self, sw):
        self.writeRegister(REG_SYNC_WORD, sw)

    def Cambiar_MapPin_irq_CAD(self,on=False):#Esta función permite cambiar los mapeos de los pines de interrupción de radio LoRa
        self.CAD_ON = on
        if self.CAD_ON:
            self.writeRegister(REG_DIO_MAPPING_1, 0x02)#DIO mapping 2
        else:
            self.writeRegister(REG_DIO_MAPPING_1, 0x00)#DIO mapping 0

    def implicitHeaderMode(self, implicitHeaderMode = False):
        if self._implicitHeaderMode != implicitHeaderMode:  # set value only if different.
            self._implicitHeaderMode = implicitHeaderMode
            modem_config_1 = self.readRegister(REG_MODEM_CONFIG_1)
            config = modem_config_1 | 0x01 if implicitHeaderMode else modem_config_1 & 0xfe
            self.writeRegister(REG_MODEM_CONFIG_1, config)
    
    def onIrqPinDI0(self,callbackRX,callbackCAD):#Esta funcion permite activar la interrupcion para el pin DIO0 de LoRa
        
        self._CADDone = callbackCAD#se guarda la funcion de CAD done
        self._onReceive = callbackRX#se guarda la funcion de CAD detected
        if self.pin_RxDone:
            if callbackRX:
                self.Cambiar_MapPin_irq_CAD(False)
                self.pin_RxDone.set_handler_for_irq_on_rising_edge(handler = self.funcionPinDI0)#el pin de interrupcion se habilita como rising edge
            else:
                self.pin_RxDone.detach_irq()
    
    def onIrqPinDI1(self,callbackTimeOut,symbTimeout,callbackCAD):#Esta funcion permite activar la interrupcion para el pin DIO0 de LoRa
        #Recepcion de las funciones a ejecutar en cada interrupción
        self._CADDetected = callbackCAD
        self._onTimeout = callbackTimeOut 
        #Limites de symbTimeout
        if symbTimeout < 4:
            symbTimeout = 4
        elif symbTimeout > 255:
            symbTimeout = 255
        self.writeRegister(REG_SYMB_TIMEOUTLSB,symbTimeout)#se guarda en el registro la cantidad de signos para timeOUT
        if self.pin_RxTimeout:
            if callbackCAD and callbackTimeOut:#si hay una funcion
                self.Cambiar_MapPin_irq_CAD(False)
                self.pin_RxTimeout.set_handler_for_irq_on_rising_edge(handler = self.funcionPinDI1)#el pin de interrupcion se habilita como rising edge
            else:
                self.pin_RxTimeout.detach_irq()

    def onReceive(self, callback):#Esta funcion permite activar la interrupcion para el pin DIO0 de LoRa (txDone)
        self._onReceive = callback#Recepcion de la Funcion a ejecutar en cada interrupcion
        if self.pin_RxDone:
            if callback:#si hay una funcion
                self.writeRegister(REG_DIO_MAPPING_1, 0x00)
                self.pin_RxDone.set_handler_for_irq_on_rising_edge(handler = self.handleOnReceive)#el pin de interrupcion se habilita como rising edge
            else:
                self.pin_RxDone.detach_irq()
    
    def onTimeout(self,callback,symbTimeout):#Esta funcion permite activar la interrupcion para el pin DIO1 de LoRa (Timeout)
        # symbTimeout 4 - 255
        if symbTimeout < 4:
            symbTimeout = 4
        elif symbTimeout > 255:
            symbTimeout = 255

        self.writeRegister(REG_SYMB_TIMEOUTLSB,symbTimeout)
        self._onTimeout = callback #Recepcion de la Funcion a ejecutar en cada interrupcion

        if self.pin_RxTimeout:
            if callback:#si hay una funcion
                self.writeRegister(REG_DIO_MAPPING_1, 0x00)
                self.pin_RxTimeout.set_handler_for_irq_on_rising_edge(handler = self.handleOnTimeout)#el pin de interrupcion se habilita como rising edge
            else:
                self.pin_RxTimeout.detach_irq()

    def handleOnTimeout(self,event_source):#Esta funcion se ejecuta en la interrupcion para devolver el paquete 
        self.aquire_lock(True)              # lock until TX_Done
        irqFlags = self.getIrqFlags()#esta funcion reinicia los valores
        if ((irqFlags & IRQ_RX_TIME_OUT_MASK) == IRQ_RX_TIME_OUT_MASK):  # RX_DONE only, irqFlags should be 0x40
            # automatically standby when RX_DONE
            if self._onTimeout:
                self._onTimeout()
        self.aquire_lock(False)             # unlock in any case.
        self.collect_garbage() 
        return True

    def receive(self, size = 0):
        self.implicitHeaderMode(size > 0) #Esto permite activar el modo Cabecera Implicita en el caso que se conosca el tamaño del paquete
        if size > 0: self.writeRegister(REG_PAYLOAD_LENGTH, size & 0xff)#si es modo implicito el tamaño del payload es necesario conocerlo
        # The last packet always starts at FIFO_RX_CURRENT_ADDR
        # no need to reset FIFO_ADDR_PTR
        #en modo continuo no es necesario reiniciar la direccion de memoria FIFO
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_RX_CONTINUOUS)
    
    def receiveSingle(self,size = 0):
        self.implicitHeaderMode(size > 0) #Esto permite activar el modo Cabecera Implicita en el caso que se conosca el tamaño del paquete
        if size > 0: self.writeRegister(REG_PAYLOAD_LENGTH, size & 0xff)#si es modo implicito el tamaño del payload es necesario conocerlo
        self.writeRegister(REG_FIFO_ADDR_PTR, FifoRxBaseAddr)
        self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_RX_SINGLE)
            
    def handleOnReceive(self, event_source):#Esta funcion se ejecuta en la interrupcion para devolver el paquete 
        self.aquire_lock(True)              # lock until TX_Done
        irqFlags = self.getIrqFlags()#esta funcion reinicia los valores
        if (irqFlags == (IRQ_RX_DONE_MASK | IRQ_VALID_HEAD_MASK) ):  # RX_DONE only, irqFlags should be 0x40
            # automatically standby when RX_DONE
            if self._onReceive:
                payload = self.read_payload()#Se devuelve un payload en la funcion _onReceive 
                self._onReceive(payload)
        else : 
            if self._onReceive:
                payload = None #Se devuelve un payload en la funcion _onReceive 
                self._onReceive(payload)
        self.aquire_lock(False)             # unlock in any case.
        self.collect_garbage()
        return True

    def funcionPinDI0(self,event_source):#Esta funcion se ejecuta en la interrupcion para devolver el paquete
        if not(self.CAD_ON):
            # irqFlags = self.getIrqFlags() should be 0x50
            if (self.getIrqFlags() & IRQ_PAYLOAD_CRC_ERROR_MASK) == 0:
                if self._onReceive:
                    payload = self.read_payload()                
                    self._onReceive(self, payload)
        else:
            if self._CADDone:
                self._CADDone(self)

    def funcionPinDI1(self,event_source):#Esta funcion se ejecuta en la interrupcion para devolver el paquete 
        if not(self.CAD_ON):
            irqFlags = self.getIrqFlags()#esta funcion reinicia los valores
            if ((irqFlags & IRQ_RX_TIME_OUT_MASK) == IRQ_RX_TIME_OUT_MASK):  # RX_DONE only, irqFlags should be 0x40
                # automatically standby when RX_DONE
                if self._onTimeout:
                    self._onTimeout(self)
        else:
            if self._CADDetected:
                self._CADDetected(self)

    def receivedPacket(self, size = 0):
        irqFlags = self.getIrqFlags()

        self.implicitHeaderMode(size > 0)
        if size > 0: self.writeRegister(REG_PAYLOAD_LENGTH, size & 0xff)

        # if (irqFlags & IRQ_RX_DONE_MASK) and \
           # (irqFlags & IRQ_RX_TIME_OUT_MASK == 0) and \
           # (irqFlags & IRQ_PAYLOAD_CRC_ERROR_MASK == 0):

        if (irqFlags == IRQ_RX_DONE_MASK):  # RX_DONE only, irqFlags should be 0x40
            # automatically standby when RX_DONE
            return True

        elif self.readRegister(REG_OP_MODE) != (MODE_LONG_RANGE_MODE | MODE_RX_SINGLE):
            # no packet received.
            # reset FIFO address / # enter single RX mode
            self.writeRegister(REG_FIFO_ADDR_PTR, FifoRxBaseAddr)
            self.writeRegister(REG_OP_MODE, MODE_LONG_RANGE_MODE | MODE_RX_SINGLE)

    def read_payload(self):
        # set FIFO address to current RX address
        # fifo_rx_current_addr = self.readRegister(REG_FIFO_RX_CURRENT_ADDR)
        self.writeRegister(REG_FIFO_ADDR_PTR, self.readRegister(REG_FIFO_RX_CURRENT_ADDR))

        # read packet length
        packetLength = self.readRegister(REG_PAYLOAD_LENGTH) if self._implicitHeaderMode else \
                       self.readRegister(REG_RX_NB_BYTES)

        payload = bytearray()
        for i in range(packetLength):
            payload.append(self.readRegister(REG_FIFO))

        self.collect_garbage()
        return bytes(payload)

    def readRegister(self, address, byteorder = 'big', signed = False):
        response = self.transfer(self.pin_ss, address & 0x7f)
        return int.from_bytes(response, byteorder)

    def writeRegister(self, address, value):
        self.transfer(self.pin_ss, address | 0x80, value)

    def collect_garbage(self):
        gc.collect()
        #print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))

    def get_freqMhz(self):
        msb=self.readRegister(REG_FRF_MSB)
        mid=self.readRegister(REG_FRF_MID)
        lsb=self.readRegister(REG_FRF_LSB)
        v=(msb<<16) | (mid<< 8) | lsb
        return v/16384

    def get_mode(self):
        return self.readRegister(REG_OP_MODE) & 0x7

    def get_preamble(self):
        return (self.readRegister(REG_PREAMBLE_MSB)<<8 | self.readRegister(REG_PREAMBLE_LSB))

    def get_ocp(self, convert_mA=False):
        v = self.readRegister(REG_OCP)
        ocp_on = v >> 5 & 0x01
        ocp_trim = v & 0b11111
        if convert_mA:
            if ocp_trim <= 15:
                ocp_trim = 45. + 5. * ocp_trim
            elif ocp_trim <= 27:
                ocp_trim = -30. + 10. * ocp_trim
            else:
                assert ocp_trim <= 27
        return dict(
                ocp_on   = ocp_on,
                ocp_trim = ocp_trim
                )

    def get_lna(self):
        v = self.readRegister(REG_LNA)
        return dict(
                lna_gain     = v >> 5,
                lna_boost_lf = v >> 3 & 0b11,
                lna_boost_hf = v & 0b11
            )

    def get_fei(self):
        msb = self.readRegister(0x28) & 0x0F
        mid = self.readRegister(0x29)
        lsb = self.readRegister(0x2a)
        freq_error = lsb + 256 * (mid + 256 * msb)
        return freq_error*self.parameters['signal_bandwidth']*2**24/(500.0*32E6) #Error Estimado para la frecuencia dada
        #ver registros para mas información y considerar la freq de clock de lora de 32Mhz

    def get_configs(self):
        
        cnf1=self.readRegister(REG_MODEM_CONFIG_1)
        cnf2=self.readRegister(REG_MODEM_CONFIG_2)
        cnf3=self.readRegister(REG_MODEM_CONFIG_3)
        time_out_lsb=self.readRegister(REG_SYMB_TIMEOUTLSB)
        symb_time_out= (cnf3&0x3)<< 8 | time_out_lsb
        
        return {'Bw':cnf1>>4,'CR':(cnf1>>1)& 0x7,'impHeaderMod':cnf1&0x1,
        'SF':cnf2>>4,'RxCrcOn':(cnf2>>2)&0x01,'symb_time_out':symb_time_out,
        'LowDataOpt': (cnf3>>3) & 0x1, 'G_auto_lna': (cnf3>>2) & 0x1 
        }

    def get_registers(self):
        bws = ('7.8 KHz', '10.4 KHz', '15.6 KHz', '20.8 KHz', '31.25 KHz', '41.7 KHz', '62.5 KHz', '125 KHz', '250 KHz')
        crc = (None,'4/5','4/6','4/7','4/8')
        mode = ('SLEEP','STDBY','FSTX','TX','FSRX','RXCONTINUOUS','RXSINGLE','CAD')
        # only sleep mode or standby
        onoff = lambda i: 'on' if i else 'off'
        f = self.get_freqMhz()
        configs=self.get_configs()
        pa_config = self.get_pa_config(convert_dBm=True)
        ocp = self.get_ocp(convert_mA=True)
        lna = self.get_lna()
        s =  "Registros principales radio LoRa SX1276\n"
        s += " Modo               %s\n" % mode[self.get_mode()]
        s += " frecuencia         %s MHz\n" % f
        s += " coding_rate        %s\n" % crc[configs['CR']]
        s += " ancho de banda     %s\n" % bws[configs['Bw']]
        s += " spreading_factor   %s chips/symb\n" % 2**configs['SF']
        s += " implicit_hdr_mode  %s\n" % onoff(configs['impHeaderMod'])
        s += " rx_payload_crc     %s\n" % onoff(configs['RxCrcOn'])
        s += " preamble           %d\n" % self.get_preamble()
        s += " low_data_rate_opti %s\n" % onoff(configs['LowDataOpt'])
        s += " agc_auto_on        %s\n" % onoff(configs['G_auto_lna'])
        s += " symb_timeout       %s\n" % configs['symb_time_out']
        #s += " payload_length     %s\n" % self.get_payload_length()
        #s += " max_payload_length %s\n" % self.get_max_payload_length()
        s += " irq_flags_mask     %s\n" % self.get_irq_flags_mask()
        #s += " irq_flags          %s\n" % self.get_irq_flags()
        s += " pa_select          %s\n" % ('PA_BOOST' if pa_config['pa_select'] else 'RFO')
        s += " max_power          %f dBm\n" % pa_config['max_power']
        s += " output_power       %f dBm\n" % pa_config['output_power']
        s += " ocp                %s\n"     % onoff(ocp['ocp_on'])
        s += " ocp_trim           %f mA\n"  % ocp['ocp_trim']
        s += " lna_gain           %s\n" % bin(lna['lna_gain'])
        s += " lna_boost_lf       %s\n" % bin(lna['lna_boost_lf'])
        s += " lna_boost_hf       %s\n" % bin(lna['lna_boost_hf'])
        #s += " detect_optimize    %#02x\n" % self.get_detect_optimize()
        #s += " detection_thresh   %#02x\n" % self.get_detection_threshold()
        s += " sync_word          %#02x\n" % self.readRegister(REG_SYNC_WORD)
        #s += " dio_mapping 0..5   %s\n" % self.get_dio_mapping()
        #s += " tcxo               %s\n" % ['XTAL', 'TCXO'][self.get_tcxo()]
        #s += " pa_dac             %s\n" % ['default', 'PA_BOOST'][self.get_pa_dac()]
        s += " version            %#02x\n" % self.readRegister(REG_VERSION)
        return s