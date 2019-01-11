# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** //**
#@brief Write a Program to interface GNSS click with stm32f4# @version v1 .0# @author Nikhil Komalan# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** * /"""

import pyb
from pyb
import Pin, delay, UART

uart = pyb.UART(4, 115200)

def main():

  Rx = bytearray(255)
i = 0

while True:
  Data = bytearray(255)
j = 0

uart.readinto(Rx)
print(Rx)

# /* Extract the $GPGGA string */
for i in range(255):
  if (Rx[i - 5] == '$'
    and Rx[i - 4] == 'G'
    and Rx[i - 3] == 'P'
    and Rx[i - 2] == 'G'
    and Rx[i - 1] == 'G'
    and Rx == 'A'):
    break

i = i - 5# // set the value at the '$'
# /* Copy string to another array */

for i in range(255):
  Data[j] = Rx
if (Rx == '\r'
  and Rx[i + 1] == '\n'):
  break
j += 1

# /* check gps status */
if (Data[17] == ','
  and Data[18] == ','
  and Data[19] == ','
  and Data[20] == ','
  and Data[21] == ','):

  print("No Fixed Position")
print("D7", Data[7], "D8", Data[8], "D9", Data[9], "D10", Data[10], "D11", Data[11], "D12", Data[12])

elif(Data[43] == '1'): # // Gps fixed data[43] = 1 otherwise 0
  print("UTC Time:", Data[7], Data[8], Data[9], Data[10], Data[11], Data[12])

if (Data[28] == 'S'):
  print("Latitude:", Data[18], Data[19], Data[20], Data[21], Data[23], Data[24], Data[25], Data[28])

else :
  print("Latitude:", Data[18], Data[19], Data[20], Data[21], Data[23], Data[24], Data[25], Data[28])

if (Data[41] == 'W'):
  print("Longitude:", Data[30], Data[31], Data[32], Data[33], Data[34], Data[36], Data[37], Data[38], Data[41])

else :
  print("Longitude:", Data[30], Data[31], Data[32], Data[33], Data[34], Data[36], Data[37], Data[38], Data[41])

print("Satellites in view: ", Data[45])

while True:
  main()