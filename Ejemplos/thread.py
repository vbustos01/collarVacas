import _thread
import time
import cola
#isActive = False
colamsn=cola.cola()
colamsn
def th_func():
	while True:	
		#while isActive:
		while colamsn.vacia():
				pass;
		print("paso función bloqueante")
		print(colamsn.extraer())
		print("estaba en cola")
		#time.sleep(delay)
		#print('Running thread {0}, time: {1} \n'.format(id, time.ticks_ms()))
		#_thread.exit()

#for i in range(2):
#    _thread.start_new_thread(th_func, (1, i))
_thread.start_new_thread(th_func,())


"""
try:
	while 1:
		pass
except KeyboardInterrupt as e:
	isActive=False
	raise e
"""