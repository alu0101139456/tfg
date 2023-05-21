

def saveInFile( input ):
    file_info.write(input + '\t')


nameGlobal = 'test'
time_test = 3
time_control = 3
com_port = 'COM3'
bps = 115200
device = 'INTEL'
filter_samples = 10
graphs = 'TRUE'

path = f"{os.getcwd()}\{device}\{nameGlobal}\{nameGlobal}"
path_info = f"{path}_info.txt"
file_info = open(path_info, 'w')

info = (
    f"Parameters to use:\n"
    f"Device: {device}\n"
    f"Time testing(sec): {time_test}\n"
    f"Port COM Arduino Board: {com_port}\n"
    f"Bits per second of COM: {bps}\n"
    f"Number of samples to filter: {filter_samples}\n"
    f"Create graphs: {graphs}"
)