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


def getMetrics( time_aux ):
    time_trans = 0
    muestras=0
    tiempo_inicial = time.time()
    while time_trans <= time_aux:    
        print(time_trans)
        muestras += 1
        tiempo_final = time.time()
        time_trans = tiempo_final - tiempo_inicial

    muestras_ps = muestras/time_trans

    print("El tiempo transcurrido es:", time_trans, "segundos")
    print("Muestras por segundo:", muestras_ps)
    print("Muestras obtenidas: ", muestras)


getMetrics(60)