
import serial
import re
import time


com_port = 'COM3'
bps = 115200

arduinoSerial       = serial.Serial(com_port , bps)
sensitivity         = 0.068

samples = 0

while ( samples < 100 ): 

        arduinoSerial.flush()
        arduinoSerial.flush()
        voltage = arduinoSerial.readline().decode('iso-8859-1').rstrip()    
        current_sensor = int(re.sub('[^0-9]', '', voltage)) * (5 / 1023)
        current = arduinoSerial.readline().decode('iso-8859-1').rstrip()
        voltage_sensor = "{:.3f}".format( int(re.sub('[^0-9]', '', current)) * (25.0 / 1023.0) )
        adjust_intensity = "{:.3f}".format( 0.32 + (current_sensor - 2.5) / sensitivity  )

        print("crudo: ", voltage)
        print("intensidad: ", adjust_intensity)
        print("voltaje",  voltage_sensor)
        samples += 1
        time.sleep(1)