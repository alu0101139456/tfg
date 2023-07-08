import serial
import argparse
import os 
import re
import subprocess
import time
from time import ctime
import datetime
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
    if (multi_core == 'FALSE'):
            arg = 'g_CinebenchCpu1Test=true'
    else:
            arg = 'g_CinebenchCpuXTest=true'
    if (device == 'INTEL'):
        cinebench_path = r'D:/Downloads/CinebenchR23/Cinebench.exe'
        bench = subprocess.Popen([cinebench_path, arg],  stderr=subprocess.PIPE) 
    else:
        bench = subprocess.Popen(['open', '/Applications/Cinebench.app',  '--args', arg])
    
    return bench

        
    
def closeBench():
    if (device == 'INTEL'):
        program = 'Cinebench.exe'
    else:
        program = "Cinebench"
    
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == program:
            # Force close program 
            proc.kill()
    

def applyFilter(df, nfilter):

    avg_volage, avg_current , value = 0, 0, 0
    for i in range( len(df["Intensidad"]) ):
        
        if ( value < nfilter ):
            avg_current += df["Intensidad"][i]
            avg_volage += df["Voltaje"][i] 
            value += 1
        else:
            writeInFile( file_filter,"{:.3f}".format(avg_current/nfilter), "{:.3f}".format(avg_volage/nfilter), df["Tiempo"][i])
            avg_volage, avg_current , value = 0, 0, 0


def writeInFile( file_temp ,current, voltage, time_stamp):
    file_temp.write(str(current) + '\t')
    file_temp.write(str(voltage) + '\t')
    file_temp.write(str(time_stamp) + '\n')



def getTime( opt='D' ):
    date_time = datetime.datetime.now()
    if (opt == 'T'):
        return date_time.strftime('%H:%M:%S.%f')
    else:
        return date_time.strftime('%d-%H_%M')

def closeFiles():
    try:
        file_start.close()
        file_testbench.close()
        file_end.close()
    except Exception as e:
        print(f"Error closing files: {e} \u2717")
        raise



def getMetrics( file_temp, time_of_test ):
    moment = f"Metrics in: {time_of_test} sec"
    saveInFile(moment)
    print(moment)
    elapsed_time, samples, samples_ps = 0, 0, 0
    init_time = time.time()
    while ( elapsed_time <= time_of_test ): 

        arduinoSerial.flush() # clean serial
        arduinoSerial.flush() # clean serial
        voltage = arduinoSerial.readline().decode('iso-8859-1').rstrip()    
        current_sensor = int(re.sub('[^0-9]', '', voltage)) * (5 / 1023)
        current = arduinoSerial.readline().decode('iso-8859-1').rstrip()
        voltage_sensor = "{:.3f}".format( int(re.sub('[^0-9]', '', current)) * (25.0 / 1023.0) )
        adjust_intensity = "{:.3f}".format( (current_sensor - 2.5) / sensitivity  )
        
        writeInFile(file_temp, adjust_intensity, voltage_sensor, getTime('T'))       
        
        samples += 1
        final_time = time.time()
        elapsed_time = final_time - init_time

    samples_ps = samples/elapsed_time

    stamp = (
        f"\n\tElapsed time: {elapsed_time:.0f} sec\n"
        f"\tSamples obtained per second: {samples_ps:.0f}\n"
        f"\tSamples obtained: {samples:.0f}\n"
    )
    print(stamp)
    saveInFile(stamp)

def getMetricsWait( file_temp, bench ):
    moment = f"Metrics waiting"
    saveInFile(moment)
    print(moment)
    elapsed_time, samples, samples_ps = 0, 0, 0
    init_time = time.time()
    while ( bench.poll() is None ): 

        arduinoSerial.flush() # clean serial
        arduinoSerial.flush() # clean serial
        voltage = arduinoSerial.readline().decode('iso-8859-1').rstrip()    
        current_sensor = int(re.sub('[^0-9]', '', voltage)) * (5 / 1023)
        current = arduinoSerial.readline().decode('iso-8859-1').rstrip()
        voltage_sensor = "{:.3f}".format( int(re.sub('[^0-9]', '', current)) * (25.0 / 1023.0) )
        adjust_intensity = "{:.3f}".format( (current_sensor - 2.5) / sensitivity  )
        
        writeInFile(file_temp, adjust_intensity, voltage_sensor, getTime('T'))    
        
        samples += 1
        final_time = time.time()
        elapsed_time = final_time - init_time

    samples_ps = samples/elapsed_time

    stamp = (
        f"\n\tElapsed time: {elapsed_time:.0f} sec\n"
        f"\tSamples obtained per second: {samples_ps:.0f}\n"
        f"\tSamples obtained: {samples:.0f}\n"
    )
    print(stamp)
    saveInFile(stamp)


def selectPortMAC():
    response = subprocess.run(['ls', '/dev/tty.*'], capture_output=True, text=True)
    print(response.stdout)
    print("Output:", response.returncode)

    print('Example: /dev/tty.usbserial-XXXXXX')
    com_port = input()
    
def saveInFile( input ):
    file_info.write( f"\n{'-'* 80}\n")
    file_info.write(input + '\t')




# Default values
time_test = 30
control_time = 10
com_port = 'COM4'
bps = 115200
device = 'INTEL'
filter_samples = 10
graphs = 'TRUE'
multi_core = 'FALSE'
wait_to_finish = 'no'
# Getting arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--device",           help="Select device [ INTEL | M1 ] [ default device: INTEL ]")
parser.add_argument("-t", "--time_test",        help="Testing time in seconds [ default time: 30 sec ]")
parser.add_argument("-c", "--control_time",     help="Control time in seconds [ default time: 3 sec ]")
parser.add_argument("-p", "--com_port",         help="Serial COM for Arduino Board [ default PORT_COM: COM3 ]")
parser.add_argument("-b", "--bits_per_sec",     help="Serial COM bits per second [ default dps: 115200 ]")
parser.add_argument("-f", "--filter_samples",   help="Number of samples to obtain arithmetic average [ default filter_samples: 10 ]")
parser.add_argument("-g", "--graphs",           help="Create graphs[ TRUE | FALSE ] [ default: TRUE ]")
parser.add_argument("-m", "--multi_core",       help="Multicore [ TRUE | FALSE ] [ default: FALSE ]")
parser.add_argument("-w", "--wait_to_finish",   help="Wait normal launch [ yes | no ] [ default: no ]")



args = parser.parse_args()
# Global variables
device          = args.device if args.device else device
time_test       = args.time_test if args.time_test else time_test
control_time    = args.control_time if args.control_time else control_time
com_port        = args.com_port if args.com_port else com_port
bps             = args.bits_per_sec if args.bits_per_sec else bps
filter_samples  = args.filter_samples if args.filter_samples else filter_samples
graphs          = args.graphs if args.graphs else graphs
multi_core      = args.multi_core if args.multi_core else multi_core
wait_to_finish  = args.wait_to_finish if args.wait_to_finish else wait_to_finish

try:    
    if (multi_core == "FALSE"):
        nameGlobal = getTime()
    else:
        nameGlobal = f"{getTime()}_m"
    
    if not os.path.exists(device): os.mkdir(device)
    
    #Paths and create folder
    if ( device == 'INTEL'):
        os.mkdir(f"{device}\\{nameGlobal}")
        path = f"{os.getcwd()}\{device}\{nameGlobal}\{nameGlobal}"
    else:
        os.mkdir(f"{device}/{nameGlobal}")
        path = f"{os.getcwd()}/{device}/{nameGlobal}/{nameGlobal}"
        
    
    path_testbench  = f"{path}_testbench.csv"
    path_start      = f"{path}_start.csv"
    path_end        = f"{path}_end.csv"
    path_global     = f"{path}_global.csv"
    path_filter     = f"{path}_filter.csv"
    path_info       = f"{path}_info.txt"

    info = (
        f"\tParameters used:\n"
        f"\t{'-'* 16}\n"
        f"\tDevice: {device}\n"
        f"\tMulti-Core: {multi_core}\n"
        f"\tWait until end testbench: {wait_to_finish}\n"
        f"\tTime testing(sec): {time_test}\n"
        f"\tTime control(wait in start/end): {control_time}\n"
        f"\tPort COM Arduino Board: {com_port}\n"
        f"\tBits per second of COM: {bps}\n"
        f"\tNumber of samples to filter: {filter_samples}\n"
        f"\tCreate graphs: {graphs}\n"
    )
    print(info)
    print("Openning files.")
    #Open files
    try:
        file_testbench  = open(path_testbench, 'w')
        file_start      = open(path_start, 'w')
        file_end        = open(path_end, 'w')
        file_filter     = open(path_filter, 'w')
        file_info       = open(path_info, 'w')
        print("\tFiles opened. \u2713")
    except Exception as e:
        print(f"Error opening files: {e} \u2717")
        raise


        
    saveInFile(info)

    #Setting varialbes
    columns=['Intensidad', 'Voltaje', 'Tiempo']

    try:
        arduinoSerial       = serial.Serial(com_port , bps)
    except Exception as e:
        print(f"Error opening serial connection with Arduino: {e} \u2717")
        raise

    sensitivity         = 0.068 if device == 'INTEL' else 0.165
    adjust_intensity    = 0.0 
    voltage_sensor      = 0.0


    try:
        getMetrics(file_start, int(control_time))    
    except Exception as e:
        print(f"Error during initial sampling: {e} \u2717")
        raise


    try:
        cine = launchBench()
    except Exception as e:
        print(f"Error during launch testbench: {e} \u2717")
        raise


    try:
        if (wait_to_finish == 'no'):
            getMetrics(file_testbench, int(time_test))
        else:
            getMetricsWait(file_testbench, cine)
    except Exception as e:
        print(f"Error during test sampling: {e} \u2717")
        raise


    try:
        closeBench()
    except Exception as e:
        print(f"Error closing testbench: {e} \u2717")
        raise


    try:
        getMetrics(file_end, int(control_time))
    except Exception as e:
        print(f"Error during final sampling: {e} \u2717")
        raise


    closeFiles()

    #Open panda
    print("Read files CSV in panda")
    try:
        df_start        = pd.read_csv(path_start,  sep='\t', header=None, names=columns)
        df_testbench    = pd.read_csv(path_testbench,  sep='\t', header=None, names=columns)        
        df_end          = pd.read_csv(path_end,  sep='\t', header=None, names=columns)
        print("\tFiles read successfully. \u2713")
    except Exception as e:
        print(f"Error reading CSV files: {e} \u2717")
        raise


    #Concatenated in global file
    print("Joining files")
    try:
        global_test = pd.concat([ df_start, df_testbench, df_end], ignore_index=True)
        global_test.to_csv(path_global, index=False, sep='\t', float_format='%.3f', header=None)
        print("\tFiles concatenated. \u2713")
    except Exception as e:
        print(f"File concatenation error: {e}  \u2717")
        raise


    try:
        global_testbench = pd.read_csv(path_global,  sep='\t', header=None, names=columns)
    except Exception as e:
        print(f"Error reading CSV files: {e} \u2717")
        raise


    print("Applying filter")
    try:
        applyFilter(global_test, filter_samples)
        file_filter.close()
        df_filter = pd.read_csv(path_filter,  sep='\t', header=None, names=columns)
        print("\tFilter applied. \u2713")
    except Exception as e:
        print(f"File concatenation error: {e}  \u2717")
        raise


    if (graphs == 'TRUE'):    
        print("Creating graphs. This may take a few minutes...")
        try:
            makeGraphic(global_testbench,path_global)
            print("\tGraph global completed. \u2713")
            makeGraphic(df_filter,path_filter)
            print("\tGraph with filter completed. \u2713")
        except Exception as e:
            print(f"Error making graphs: {e} \u2717")
            raise


    try:
        arduinoSerial.close()
    except Exception as e:
        print(f"Error closing Arduino serial : {e} \u2717")
        raise

    file_info.close()
    file_filter.close()
    print("\nProcess completed successfully!!!\n")
except:
    if args.help is not None:
        closeFiles()
        file_info.close()
        file_filter.close()
        dir_rm = f"{device}/{nameGlobal}"
        if (device == 'INTEL'):
            subprocess.run(["powershell.exe", f'Remove-Item "{device}/{nameGlobal}" -Recurse -Confirm:$false'], shell=True)
        else:
            os.system(f"rm {device}/{nameGlobal}")
    
    print(f"Ejecution stoped \u2717")