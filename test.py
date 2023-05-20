
import psutil
import subprocess
import os
import time
from time import ctime
import datetime
import pandas as pd

def getTime( opt='D' ):
    date_time = datetime.datetime.now()
    if (opt == 'T'):
        return date_time.strftime('%H:%M:%S.%f')
    else:
        return date_time.strftime('%d-%H_%M')
    
def writeInFile( file_temp, oio):
    file_temp.write(str(oio) + '\t')


device = 'INTEL'

nameGlobal = getTime()
filename = f'{nameGlobal}.csv'

file_testbench = open(f"{os.getcwd()}\\{device}\\{nameGlobal}_testbench.csv", 'w')
file_start = open(f"{os.getcwd()}\\{device}\\{nameGlobal}_start.csv", 'w')
file_end = open(f"{os.getcwd()}\\{device}\\{nameGlobal}_end.csv", 'w')




for i in range(20):
    writeInFile(file_start, 'inicio\n')

for i in range(20):
    writeInFile(file_testbench, 'test\n')
    
for i in range(20):
    writeInFile(file_end, 'fin\n')



file_testbench.close()
file_start.close()
file_end.close()

dfI = pd.read_csv(f"{os.getcwd()}\\{device}\\{nameGlobal}_testbench.csv")
dfT = pd.read_csv(f"{os.getcwd()}\\{device}\\{nameGlobal}_start.csv")
dfF = pd.read_csv(f"{os.getcwd()}\\{device}\\{nameGlobal}_end.csv")

global_test = pd.concat([ dfI, dfT, dfF], ignore_index=True)

global_test.to_csv(f"{os.getcwd()}\\{device}\\{nameGlobal}_global.csv", index=False)