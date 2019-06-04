from gps_upy import Gps_upy
import _thread

gps = Gps_upy()
def treadsito():
	while 1:
		if gps.any() != None:
		gps_payload[] = gps.req_position()
		if gps_payload[0]:
			pos = gps_payload[1]
			break

gps.periodic_mode()
_thread.start_new_thread(treadsito, ())