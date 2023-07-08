
import serial
import re
import time


com_port = 'COM3'
bps = 115200

arduinoSerial       = serial.Serial(com_port , bps)
# sensitivity         = 0.068 # Intel
sensitivity           = 0.165 # MAC
samples = 0

while ( samples < 2000 ): 

  arduinoSerial.flush()
  arduinoSerial.flush()
  vol_current = int(arduinoSerial.readline().decode('iso-8859-1').strip()) * (5 / 1023.0)
  if vol_current:
    current =  "{:.3f}".format( (vol_current - 2.5) / sensitivity )
  vol_vol = "{:.3f}".format( int(arduinoSerial.readline().decode('utf-8').strip()) * (25.0 / 1023.0) )

  print("Corriente: ", current)
  # print("intensidad: ", adjust_intensity)
  print("Voltaje: ",  vol_vol)
  samples += 1
  # time.sleep(1) 