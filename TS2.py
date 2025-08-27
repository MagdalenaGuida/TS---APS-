# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 12:34:31 2025

@author: magui
"""


import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import wmi

fs =50000     # Frecuencia de muestreo
N = 50000     # Número de muestras
ts = 1 / fs  # Tiempo entre muestras correlativas
# tiempo total de muestreo = N*ts = N * 1/fs = 1s
df = fs/N  # Resolución espectral  en Hz 
dc = 0       #Desplazamiento vertical [V]  
ph = 0       #FASE = Desplazamiento horizontal [rad]


# Definicion funciónes seno
def func_sen(Vmax=1, dc=dc, ff=1, ph=ph, nn=N, fs=fs):
    
    tt = np.arange(0, nn / fs, 1 / fs).reshape(nn,1)
    
    xx = Vmax * np.sin(2 * np.pi * ff * tt + ph).reshape(nn,1) + dc
    
    return tt, xx

def func_cos(Vmax=1, dc=dc, ff=1, ph=ph, nn=N, fs=fs):
    
    tt = np.arange(0, nn / fs, 1 / fs).reshape(nn,1)
    
    xx = Vmax * np.sin(2 * np.pi * ff * tt + ph + np.pi/2).reshape(nn,1) + dc
    
    return tt, xx
#Defino el coseno como el seno con un desfasaje de pi/2 'impuesto', pq sen(x + pi/2) = cos(x)


# Definicion funcion cuadrada
def func_square(Vmax=1, dc=dc, ph=ph, nn=N, fs=fs, ff=1, duty= 1/2):
   
    tta = np.arange(0, nn/fs, 1/fs).reshape(nn, 1)
    
    xxa = Vmax * signal.square(2 * np.pi * tta * ff + ph, duty=duty ).reshape(nn, 1) + dc
    
    return tta, xxa

def correlacion( x , y ):
    
    if len(x) != len(y):
        raise ValueError ("Las señales deben tener el mismo largo")
    
    n = len(x)
    x = x.reshape(-1)
    y = y.reshape(-1)
    corr = np.correlate(x, y, mode='full') / np.max(np.correlate(x, y, mode='full'))
    
    k = np.arange(-n + 1 , n)
    
    return k, corr


tt1, xx1 = func_sen(ff=2000, fs=fs)                    # senoidal 'base'
tt2, xx2 = func_sen( ff= 2000, ph= np.pi/2, Vmax=3)    # amplificada  y defazada
tt3, xx3 = func_sen(ff=1000, ph= np.pi/2, Vmax=3)      # senoidal con mitad de f 
xx4 = xx3 * xx1                                        # modulada 
xx5 = np.clip(xx1,a_min = -.75, a_max= 0.75)           # funcion de amp=1 reducida a su 75%    
# # como la amplitud es 1, el 75% va a ser 0.75

tta1, xxa1 = func_square(ff= 4000) 

tta2 = np.arange(0, N/fs, 1/fs).reshape(N, 1)
xxa2 = np.where(tta2 < 0.01 , 1, 0)

recorte = int(0.002 * fs)      # 2 ms
recorte2 = int(0.03 * fs )
tt1 = tt1[:recorte]
xx1 = xx1[:recorte]
tt2 = tt2[:recorte]
xx2 = xx2[:recorte]
tt4 = tt1[:recorte]
xx4 = xx4[:recorte]
xx5 = xx5[:recorte]
tta1 =tta1[:recorte]
xxa1 = xxa1[:recorte]
tta2 = tta2[:recorte2]
xxa2 = xxa2[:recorte2]
                          

#%%

# GRAFICO 
# Caracteristicas del Grafico
plt.figure()
plt.title(f"Señales Senoidales, nro de muestras={N}, tiempo entre muestras={ts}")

plt.plot(tt1, xx1, label="Frecuencia = 2kHz Hz", color = 'b')
plt.plot(tt2, xx2, label="Frecuencia = 2kHz, ph=pi/2,amplificada", color= 'g')
plt.plot(tt1, xx4, label="Senoidal modulada", color = 'y')
plt.plot(tt1, xx5, label="Senoidal al 75% de amplitud", color='orange')
plt.legend(loc = 'lower left')
plt.xlabel("Tiempo [segundos]")
plt.ylabel("Amplitud [Volts]")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure()
plt.title(f"Señal cuadrada, nro de muestras={N}, tiempo entre muestras={ts}")

plt.plot(tta1, xxa1, label="Señal cuadrada f =4000Hz")
plt.legend(loc = 'lower left')
plt.xlabel("Tiempo [secs]")
plt.ylabel("Amp [Volts]")
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure()
plt.title(f"Señal pulso, nro de muestras={N}, tiempo entre muestras={ts}")

plt.plot(tta2, xxa2, label="Señal pulso")
plt.legend(loc = 'lower left')
plt.xlabel("Tiempo [secs]")
plt.ylabel("Amp [Volts]")
plt.grid(True)
plt.tight_layout()
plt.show()

 #%% 
## 2)  VERIFICAR ORTOGONALIDAD 
## Compruebo que el producto interno de cero, 

print("2) VERIFICAR ORTOGONALIDA:")
area12 = np.dot(xx1.T, xx2 )
print(f"Producto interno entre la primer senoidal y la segunda: {area12}")

area14 = np.dot(xx1.T , xx4)
print(f"Producto interno entre la primer senoidal y la modulada: {area14}")

area15 = np.dot(xx1.T,  xx5)
print(f"Producto interno entre la primer senoidal y la de amplitud al 75%: {area15}")


#%% 3) AUTOCORRELACION Y CORRELACION 

k1, corr1 = correlacion (xx1, xx1)                ## autocorrelacion !!
k2, corr2 = correlacion (xx1, xx2)
k4, corr4 = correlacion (xx1, xx4)
k5, corr5 = correlacion (xx1, xx5)


plt.figure()
plt.title("Correlacion y Autocorrelacion de Señales Senoidales")

plt.plot(k1 * ts, corr1, label="Autocorrelacion", color = 'b')
plt.plot(k2 * ts, corr2, label="Correlacion con Sen 2", color= 'g')
plt.plot(k4 * ts, corr4, label="Correlacion con Sen 3", color = 'y')
plt.plot(k5 * ts, corr5, label="Correlacion con Sen 4", color='orange')
plt.legend(loc = 'lower left')
plt.xlabel("Tiempo [segundos]")
plt.ylabel("Amplitud [Volts]")
plt.grid(True)
plt.tight_layout()
plt.show()


#%%
## 4) 
falpha = 4 
fbeta = falpha / 2
f1 = falpha - fbeta 
f2 = falpha + fbeta 

tt4a, xx4a = func_sen(ff= falpha)
tt4b, xx4b = func_sen(ff= fbeta) 
tt4c, xx4c = func_cos(ff = f1)
tt4d, xx4d = func_cos(ff = f2)
xxizq = 2 * xx4a * xx4b
xxder = xx4c - xx4d
igualdad = xxizq - xxder 

### GRAFICO 
plt.figure()
plt.title("4) Demostracion igualdad")

plt.plot(tt4a, xxizq, label=" 2*sen(alpha)*sen(beta)", color = 'b')
plt.plot(tt4a, xxder, label=" cos(alpha-beta) - cos(alpha+beta)", color= 'r', linestyle = '--')
plt.plot(tt4a, igualdad, label=" Resta punto a punto ", color = 'y')

plt.legend(loc = 'lower left')
plt.xlabel("Tiempo [segundos]")
plt.ylabel("Amplitud [Volts]")
plt.grid(True)
plt.tight_layout()
plt.show()






