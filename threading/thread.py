import _thread
import time

isActive = True

def th_func(delay, id):
    while isActive:
        time.sleep(delay)
        print('Running thread {0}, time: {1} \n'.format(id, time.ticks_ms()))
	#_thread.exit()

for i in range(2):
    _thread.start_new_thread(th_func, (1, i))


"""
try:
	while 1:
		pass
except KeyboardInterrupt as e:
	isActive=False
	raise e
"""