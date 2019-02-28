def joinbytes(buf): #el buffer es el leido a partir del i2s, fijado a 4 bytes por palabra 
	resultado=list()
	for i in range(0,len(buf),4):
		# son 4 bytes: MSB(8b)+B(8b)+LSB(2b+ceros(6b))+dontcare(8b)
		# por esto, no se toma en cuenta el 4to byte del buffer por iteracion
		resultado.append((buf[i+2]<<8)|(buf[i+3]))
	return resultado

def twocomp2dec(lista,bits):#convierte una lista en complemento de 2 a decimal, 
							#tomando en cuenta la cantidad de bits de la palabra
	mask = 0xffffffff >> (32-bits)
	for i in range(len(lista)):
		if((lista[i] & mask)>>(bits-1)):
			lista[i]=-(((lista[i] & mask) ^ mask)+1)

def gen_wav_header( #expropiado y matuteado de @miketeachman
    sampleRate,
    bitsPerSample,
    channels,
    samples,
    ):
    datasize = samples * channels * bitsPerSample // 8
    o = bytes('RIFF', 'ascii')  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4, 'little')  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes('WAVE', 'ascii')  # (4byte) File type
    o += bytes('fmt ', 'ascii')  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data
    o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM)
    o += channels.to_bytes(2, 'little')  # (2byte)
    o += sampleRate.to_bytes(4, 'little')  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,
            'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2, 'little')  # (2byte)
    o += bitsPerSample.to_bytes(2, 'little')  # (2byte)
    o += bytes('data', 'ascii')  # (4byte) Data Chunk Marker
    o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes
    return o

def prune(samples_in, samples_out):
    for i in range(len(samples_in) // 8):
        samples_out[2*i] = samples_in[8*i + 2]
        samples_out[2*i + 1] = samples_in[8*i + 3]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
  
#def grabar(sdcard,filename='mic_record',duration=5,fs=8000)