from machine import I2S

class Mic():
	def __init__(self):
		self.SAMPLE_BLOCK_SIZE = 24
		self.SAMPLES_PER_SECOND = 32000
		
		audio_mic = I2S(
		I2S.NUM0,
		bck = 25,
		ws = 27,
		sdin = 26,
		mode = I2S.MASTER_RX,
		samplerate = self.SAMPLES_PER_SECOND,
		dataformat = I2S.B32,
		channelformat = I2S.RIGHT_LEFT,
		standard = I2S.PHILIPS,
		dmacount = 64,dmalen=128)

