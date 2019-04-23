from machine import I2S, Pin, SPI
from drivers import sdcard
import utime, uos

class Mic(object):
	"""docstring for Mic"""

	SDCARD_SECTOR_SIZE = 512                    # typical sector size for SDCards, in bytes
	SAMPLE_BLOCK_SIZE = SDCARD_SECTOR_SIZE * 4  #  
	BYTES_PER_SAMPLE = 2
	BITS_PER_SAMPLE = 16
	SAMPLES_PER_SECOND = 4000
	RECORD_TIME_IN_SECONDS = 4

	def __init__(self):
		super(Mic, self).__init__()

		
		self.vext_pin = Pin(21, Pin.OUT, value=0)
		self.cs_lora = Pin(18,Pin.OUT, value=1)
		self.initMic()

		"""
		self.audio = I2S(I2S.NUM0, bck=bck_pin, ws=ws_pin, sdin=sdin_pin, 
              standard=I2S.PHILIPS, mode=I2S.MASTER_RX,
              dataformat=I2S.B32, channelformat=I2S.ONLY_RIGHT,
              samplerate=Mic.SAMPLES_PER_SECOND*2,
              dmacount=8, dmalen=256)
		"""
		self.spi = SPI(sck=Pin(23), mosi=Pin(12), miso=Pin(14))
	"""
	
	"""
	def sleep(self, state):
		if state is True:
			self.audio.deinit()
			#self.cs_lora.value(1)
		else:
			self.initMic()
			#self.cs_lora.value(0)

	def record(self, duration = 4):
		self.sleep(False)
		WAV_DATA_SIZE = duration * Mic.SAMPLES_PER_SECOND * Mic.BYTES_PER_SAMPLE
		wav_header = self.gen_wav_header(Mic.SAMPLES_PER_SECOND, Mic.BITS_PER_SAMPLE, 1, Mic.SAMPLES_PER_SECOND * duration)
		if self.initSD() is True:
			f = open('/sd/mic_recording.wav','wb')
			f.write(wav_header)

			now = utime.ticks_ms()

			mic_samples = bytearray(Mic.SAMPLE_BLOCK_SIZE)
			sd_samples = bytearray(Mic.SDCARD_SECTOR_SIZE)
			numread = 0
			numwrite = 0

			for _ in range(WAV_DATA_SIZE // Mic.SDCARD_SECTOR_SIZE):
			    try:
			        numread += self.audio.readinto(mic_samples)    
			        self.prune(mic_samples, sd_samples)
			        numwrite += f.write(sd_samples)
			    except KeyboardInterrupt:  
			        break
			f.close()
			uos.umount("/sd")
			self.spi.deinit()
			self.sleep(True)
			print("Listo, bytes leídos: {}, bytes escritos: {}, duración: {}".format(numread,
																				numwrite,
																				utime.ticks_diff(utime.ticks_ms(),now)))
		else:
			print("Fallo la grabación")

	def initSD(self):
		counter = 0
		while counter < 3:
			try:
			    sd = sdcard.SDCard(self.spi, Pin(2,Pin.OUT))
			    vfs =uos.VfsFat(sd)
			    uos.mount(vfs, "/sd")
			    return True
			except Exception as e:
			    print("Error al montar sd, intento: "+str(counter))
			    self.spi.deinit()
			counter += 1
		return False

	def initMic(self):
		try:
			self.bck_pin = Pin(25, Pin.IN)
			self.ws_pin = Pin(27, Pin.IN)
			self.sdin_pin = Pin(35)
			self.audio = I2S(I2S.NUM0, bck=self.bck_pin, ws=self.ws_pin, sdin=self.sdin_pin, 
              standard=I2S.PHILIPS, mode=I2S.MASTER_RX,
              dataformat=I2S.B32, channelformat=I2S.ONLY_RIGHT,
              samplerate=Mic.SAMPLES_PER_SECOND*2,
              dmacount=8, dmalen=256)
		except ValueError:
			print("El puerto ya esta iniciado, hard reset para funcionar...")


	def prune(self, samples_in, samples_out):
	    for i in range(len(samples_in) // 8):
	        samples_out[2*i] = samples_in[8*i + 2]
	        samples_out[2*i + 1] = samples_in[8*i + 3]    

	def gen_wav_header(self, sampleRate, bitsPerSample, num_channels, num_samples):
	    datasize = num_samples * num_channels * bitsPerSample // 8
	    o = bytes("RIFF",'ascii')                                                   # (4byte) Marks file as RIFF
	    o += (datasize + 36).to_bytes(4,'little')                                   # (4byte) File size in bytes excluding this and RIFF marker
	    o += bytes("WAVE",'ascii')                                                  # (4byte) File type
	    o += bytes("fmt ",'ascii')                                                  # (4byte) Format Chunk Marker
	    o += (16).to_bytes(4,'little')                                              # (4byte) Length of above format data
	    o += (1).to_bytes(2,'little')                                               # (2byte) Format type (1 - PCM)
	    o += (num_channels).to_bytes(2,'little')                                    # (2byte)
	    o += (sampleRate).to_bytes(4,'little')                                      # (4byte)
	    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
	    o += (num_channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
	    o += (bitsPerSample).to_bytes(2,'little')                                   # (2byte)
	    o += bytes("data",'ascii')                                                  # (4byte) Data Chunk Marker
	    o += (datasize).to_bytes(4,'little')                                        # (4byte) Data size in bytes
	    return o