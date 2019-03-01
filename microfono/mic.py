from machine import I2S

SAMPLE_BLOCK_SIZE = 24
SAMPLES_PER_SECOND = 32000

bck_mic_pin = 25
ws_mic_pin = 27
sdin_mic_pin = 26

audio_mic=I2S(I2S.NUM0,bck=bck_mic_pin,ws=ws_mic_pin,sdin=sdin_mic_pin,mode=I2S.MASTER_RX,
	samplerate=SAMPLES_PER_SECOND, dataformat=I2S.B32,
	channelformat=I2S.RIGHT_LEFT,standard=I2S.PHILIPS,
	dmacount=64,dmalen=128)

samples = bytearray(SAMPLE_BLOCK_SIZE)

numread = audio_mic.readinto(samples)