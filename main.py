import serial
import argparse
import os 
import re
import subprocess
import time
from time import ctime
import ntplib
import datetime
import pytz
import psutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def makeGraphic(df,path): 

    # plt.style.use('_mpl-gallery')
    plt.figure(figsize=(20, 16))
    plt.plot(df['Tiempo'], df['Intensidad'])
    plt.xlabel('Tiempo')
    plt.ylabel('Intensidad')
    plt.title('Consumo energético')

    x_values = df['Tiempo']
    step = len(x_values) // 30
    ticks = x_values[::step]
    plt.xticks(ticks, rotation='vertical')
    whitout_ext = path.split('.')[0]
    png_name = f'{whitout_ext}.png'
    plt.savefig(png_name, dpi=300, bbox_inches='tight')


def launchBench():
    if (device == 'INTEL'):
        cinebench_path = r'D:/Downloads/CinebenchR23/Cinebench.exe'
        subprocess.Popen([cinebench_path, 'g_CinebenchCpu1Test=true'],  stderr=subprocess.PIPE) 
    else:
        subprocess.Popen(['open', '/Applications/Cinebench.app',  '--args', 'g_CinebenchCpu1Test=true'])

        
    
def closeBench():
    if (device == 'INTEL'):
        program = 'Cinebench.exe'
    else:
        program = "Cinebench"
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == program:
            # Cerramos el proceso 
            proc.kill()
    

def applyFilter(df, nfiltro):

    value = 0
    mediaVoltaje = 0
    mediaIntensidad = 0
    for i in range( len(df["Intensidad"]) ):
        
        if ( value < nfiltro ):
            mediaIntensidad += df["Intensidad"][i]
            mediaVoltaje += df["Voltaje"][i] 
            value += 1
        else:
            writeInFile( file_filter,"{:.3f}".format(mediaIntensidad/nfiltro), "{:.3f}".format(mediaVoltaje/nfiltro), df["Tiempo"][i])
            mediaVoltaje = 0
            mediaIntensidad = 0
            value = 0


def writeInFile( file_temp ,ajusteIntensidad, sensorVoltaje, ntp_time):
    file_temp.write(str(ajusteIntensidad) + '\t')
    file_temp.write(str(sensorVoltaje) + '\t')
    file_temp.write(str(ntp_time) + '\n')



def getTime( opt='D' ):
    date_time = datetime.datetime.now()
    if (opt == 'T'):
        return date_time.strftime('%H:%M:%S.%f')
    else:
        return date_time.strftime('%d-%H_%M')



def getMetrics( file_temp, time_aux ):
    print("Get metrics of: ", time_aux, "sec")
    time_trans = 0
    muestras=0
    tiempo_inicial = time.time()
    while time_trans <= time_aux:    

        # arduinoSerial.flush()
        # arduinoSerial.flush()
        # voltaje = arduinoSerial.readline().decode('iso-8859-1').rstrip()    
        # sensorIntensidad = int(re.sub('[^0-9]', '', voltaje)) * (5 / 1023)
        # corriente = arduinoSerial.readline().decode('iso-8859-1').rstrip()
        sensorVoltaje = "{:.3f}".format( int(re.sub('[^0-9]', '', corriente)) * (25.0 / 1023.0) )
        ajusteIntensidad = "{:.3f}".format( 0.32 + (sensorIntensidad - 2.5) / sensibilidad  )

        
        writeInFile(file_temp, ajusteIntensidad, sensorVoltaje, getTime('T'))    
        
        muestras += 1
        tiempo_final = time.time()
        time_trans = tiempo_final - tiempo_inicial

    muestras_ps = muestras/time_trans

    print("El tiempo transcurrido es:", time_trans, "segundos")
    print("Muestras por segundo:", muestras_ps)
    print("Muestras obtenidas: ", muestras)


def selectPortMAC():
    resultado = subprocess.run(['ls', '/dev/tty.*'], capture_output=True, text=True)
    print(resultado.stdout)
    print("Código de salida:", resultado.returncode)

    print('Ejemplo: /dev/tty.usbserial-XXXXXX')
    com_port = input()
    
   

# Default values
time_test = 3
time_control = 3
com_port = 'COM3'
bps = 115200
device = 'MAC'
filter_samples = 10
graphs = 'TRUE'

# Getting arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device", help="Select device [ INTEL | M1 ] [ default device: INTEL ]")
parser.add_argument("-t", "--time_test", help="Testing time in seconds [ default time: 30 sec ]")
parser.add_argument("-c", "--time_control", help="Control time in seconds [ default time: 3 sec ]")
parser.add_argument("-p", "--com_port", help="Serial COM for Arduino Board [ default PORT_COM: COM3 ]")
parser.add_argument("-b", "--bits_per_sec", help="Serial COM bits per second [ default dps: 115200 ]")
parser.add_argument("-f", "--filter_samples", help="Number of samples to obtain arithmetic average [ default filter_samples: 10 ]")
parser.add_argument("-g", "--graphs", help="Create graphs[ TRUE | FALSE ] [ default: TRUE ]")

args = parser.parse_args()

device = args.device if args.device else device
time_test = args.time_test if args.time_test else time_test
time_control = args.time_control if args.time_control else time_control
com_port = args.com_port if args.com_port else com_port
bps = args.bits_per_sec if args.bits_per_sec else bps
filter_samples = args.filter_samples if args.filter_samples else filter_samples
graphs = args.graphs if args.graphs else graphs

# if (device == 'MAC'): selectPortMAC()

print("Parameters to use: ")
print("Device: ", device)
print("Time testing(sec): ", time_test)
print("Port COM Arduino Board: ", com_port)
print("Bits per second of COM: ", bps)
print("Númber of samples to filter: ", filter_samples)
print("Create graphs: ", graphs)


nameGlobal = getTime()
filename = f'{nameGlobal}.csv'
if not os.path.exists(device): os.mkdir(device)
os.mkdir(f"{device}\\{nameGlobal}")

# Global variables
path = f"{os.getcwd()}\{device}\{nameGlobal}\{nameGlobal}"
path_testbench = f"{path}_testbench.csv"
path_start = f"{path}_start.csv"
path_end = f"{path}_end.csv"
path_global = f"{path}_global.csv"
path_filter = f"{path}_filter.csv"

#Open files
file_testbench = open(path_testbench, 'w')
file_start = open(path_start, 'w')
file_end = open(path_end, 'w')
file_filter = open(path_filter, 'w')

# arduinoSerial = serial.Serial(com_port , bps)
sensibilidad = 0.068
ajusteIntensidad = 0.0
sensorVoltaje = 0.0
tempProcessor = 0.0
muestras=0


getMetrics(file_start, int(time_control))

cine = launchBench()

getMetrics(file_testbench, int(time_test))

closeBench()

getMetrics(file_end, int(time_control))


file_start.close()
file_testbench.close()
file_end.close()



#Open panda
df_start = pd.read_csv(path_start,  sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'])
df_testbench = pd.read_csv(path_testbench,  sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'])
df_end = pd.read_csv(path_end,  sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'])



#Concatenated in global file

global_test = pd.concat([ df_start, df_testbench, df_end], ignore_index=True)
global_test.to_csv(path_global, index=False, sep='\t', float_format='%.3f', header=None)

global_testbench = pd.read_csv(path_global,  sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'])

applyFilter(global_test, filter_samples)
print("Pasando filtro")
file_filter.close()
df_filter = pd.read_csv(path_filter,  sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'])


if (graphs == 'TRUE'):    
    print("Creando gráficas. Esto puede tardar unos minutos...")
    makeGraphic(global_testbench,path_global)
    makeGraphic(df_filter,path_filter)




arduinoSerial.close()


