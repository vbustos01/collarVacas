from gps_upy import Gps_upy
import _thread

a = Gps_upy()

_thread.start_new_thread(a.leer_parasiempre, ())
_thread.start_new_thread(a.request_efemerides, ())

# dt
#super().write(b'$PMTK514,1,1,1,1,1,5,1,1,1,1,1,1,0,1,1,1,1,1,1*2A\r\n')
		