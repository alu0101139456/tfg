import os

def saveInFile( file, input ):
    print("saveinFile")



device = 'MAC'
time_test = '10:20:30'
com_port = 'COM3'
bps = 115200
filter_samples = 10
graphs = 'TRUE'
nameGlobal = '20-14_23'

if not os.path.exists(device): os.mkdir(device)
os.mkdir(f"{device}\\{nameGlobal}")
path = f"{os.getcwd()}\{device}\{nameGlobal}\{nameGlobal}.txt"
file_filter = open(path, 'w')

info = (
    f"Parameters to use:\n"
    f"Device: {device}\n"
    f"Time testing(sec): {time_test}\n"
    f"Port COM Arduino Board: {com_port}\n"
    f"Bits per second of COM: {bps}\n"
    f"Númber of samples to filter: {filter_samples}\n"
    f"Create graphs: {graphs}"
)

print(message)