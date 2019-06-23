from time import sleep


class Controller:

    class Mock:
        pass

    GPIO_PINS = []

    PIN_ID_FOR_LORA_RESET = None

    PIN_ID_FOR_LORA_SS = None
    PIN_ID_SCK = None
    PIN_ID_MOSI = None
    PIN_ID_MISO = None

    PIN_ID_FOR_LORA_DIO0 = None
    PIN_ID_FOR_LORA_DIO1 = None
    PIN_ID_FOR_LORA_DIO2 = None
    PIN_ID_FOR_LORA_DIO3 = None
    PIN_ID_FOR_LORA_DIO4 = None
    PIN_ID_FOR_LORA_DIO5 = None


    def __init__(self, pin_id_reset = PIN_ID_FOR_LORA_RESET):
        self.pin_reset = self.prepare_pin(pin_id_reset)
        self.reset_pin(self.pin_reset)
        self.transceivers = {}


    def add_transceiver(self,
                        transceiver,
                        pin_id_ss = PIN_ID_FOR_LORA_SS,
                        pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                        pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                        pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
                        pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
                        pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                        pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5):
        #transceiver.blink_led = self.blink_led
        transceiver.pin_ss = self.prepare_pin(pin_id_ss)
        transceiver.pin_RxDone = self.prepare_irq_pin(pin_id_RxDone)
        transceiver.pin_RxTimeout = self.prepare_irq_pin(pin_id_RxTimeout)
        transceiver.pin_ValidHeader = self.prepare_irq_pin(pin_id_ValidHeader)
        transceiver.pin_CadDone = self.prepare_irq_pin(pin_id_CadDone)
        transceiver.pin_CadDetected = self.prepare_irq_pin(pin_id_CadDetected)
        transceiver.pin_PayloadCrcError = self.prepare_irq_pin(pin_id_PayloadCrcError)

        self.spi = self.prepare_spi(self.get_spi())
        transceiver.transfer = self.spi.transfer

        transceiver.init()

        self.transceivers[transceiver.name] = transceiver
        return transceiver


    def prepare_pin(self, pin_id, in_out = None):
        reason = '''
            # a pin should provide:
            # .pin_id
            # .low()
            # .high()
            # .value()  # read input.
            # .irq()    # (ESP8266/ESP32 only) ref to the irq function of real pin object.
        '''
        raise NotImplementedError(reason)


    def prepare_irq_pin(self, pin_id):
        reason = '''
            # a irq_pin should provide:
            # .set_handler_for_irq_on_rising_edge()  # to set trigger and handler.
            # .detach_irq()
        '''
        raise NotImplementedError(reason)


    def get_spi(self):
        reason = '''
            # initialize SPI interface
        '''
        raise NotImplementedError(reason)


    def prepare_spi(self, spi):
        reason = '''
            # a spi should provide:
            # .close()
            # .transfer(pin_ss, address, value = 0x00)
        '''
        raise NotImplementedError(reason)

    def reset_pin(self, pin, duration_low = 0.05, duration_high = 0.05):
        pin.low()
        sleep(duration_low)
        pin.high()
        sleep(duration_high)


    def __exit__(self):
        self.spi.close()

