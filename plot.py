import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')
plt.figure(figsize=(20, 16))
df = pd.read_csv('PruebasIntel//29-20_07_filter.csv', sep='\t', header=None, names=[ 'Intensidad', 'Voltaje', 'Tiempo'] )

plt.plot(df['Tiempo'], df['Intensidad'])
plt.xlabel('Tiempo')
plt.ylabel('Intensidad')
plt.title('Título de la gráfica')


plt.savefig("TESTGRAFICA.png", dpi=600, bbox_inches='tight')