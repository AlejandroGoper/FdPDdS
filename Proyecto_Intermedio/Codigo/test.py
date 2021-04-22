#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 23:12:50 2021

@author: I. Alejandro Gómez
"""

# Este script es para recortar en frecuencia manualmente y comparar resultados

# Importando funciones utiles
from calcVectFrec import calcVecFrec
from calculaVerdaderaAmplitud import calculaVerdaderaAmplitud
from buscar_frecuencias import buscar_frecuencias
from localizador_frecuencias import localizar_maximo_entre
#Para leer los archivos de matlab
from scipy.io import loadmat
#Para fft
from numpy.fft import fft
#Para calculo numérico
from numpy import array,floor,where,sqrt,log10,round
# Para graficar
import matplotlib.pyplot as plt 

print("------------------------------------------------------")
print("    Fundamento de procesamiento digital de señales")
print("                Proyecto Intermedio               ")
print("                   Señal FDPOAE                   ")
print("------------------------------------------------------")

try:
    nombre = input("Ingrese el nombre del archivo a analizar: \n")
    direccion = "../Archive/"+nombre
    print("\nCargando...\n")
    archivo = loadmat(direccion) #Dirección del archivo .mat
except:
    print("Ha ocurrido un error al leer el archivo")
    exit()

# Guardamos en arreglos numpy los datos de los archivos .mat
data = array(archivo["Data"]) # data es una matriz pero solo queremos un array
senal = data[0] # asi que solo tomamos la primera posicion
fs =  float(archivo["fs"]) # Convertimos a escalar float el dato del archivo

print("************************************************************")
print(f"  Tamaño de los datos: {n}")
print(f"  Frecuencia de muestreo: {fs} Hz")
print("************************************************************")
#Aplicando la fft a la señal 
fft_senal = fft(senal)

#Esta señal la vamos a transformar a Decibelios SPL

# Primero calculamos la verdadera amplitud del espectro de fourier con la función
# que se dejo en la tarea  
amplitud_fft = calculaVerdaderaAmplitud(fft_senal)
#Convirtiedo a Decibelios SPL
r2 = sqrt(2)/2
P_rms = r2*amplitud_fft
amplitud_fft_db = 20*log10(P_rms/(20*10**-6))

# Calculamos el vector de frecuencias, recordemos que la función calcVecFrec
# requiere como parametros la señal y el periodo de muestreo que es el inverso
# de la frecuencia de muestreo fs
vfrec = calcVecFrec(senal,1/fs)

# Calculamos el  vector de frecuencias para la gráfica de amplitudes verdaderas de la fft
n = len(fft_senal)
if(n%2 == 0):
    lim = floor(n/2)
else:
    lim = floor(n/2)+1
vfreqpos = vfrec[0:int(lim)]

# Algoritmo principal
print("Introduza manualmente el intervalo en frecuencia donde creee que puedan localizarse F1 y F2")
f_corte_inf = float(input("Frecuencia limite inferior: "))
f_corte_sup = float(input("Frecuencia limite superior: "))
ind_f_corte_inf = where(vfreqpos == f_corte_inf)
ind_f_corte_inf = int(ind_f_corte_inf[0])
ind_f_corte_sup = where(vfreqpos == f_corte_sup)
ind_f_corte_sup = int(ind_f_corte_sup[0])
    
    #Limitando el espectro de frecuencias 
vfreqpos_cortada = vfreqpos[ind_f_corte_inf:ind_f_corte_sup]
amplitud_fft_db_cortada = amplitud_fft_db[ind_f_corte_inf:ind_f_corte_sup]
f1_c, f2_c = buscar_frecuencias(amplitud_fft_db_cortada, vfreqpos_cortada, 10)
ind_f1_c = where(vfreqpos_cortada == f1_c)
ind_f2_c = where(vfreqpos_cortada == f2_c)
    #Aqui solo añadimos el indice de la frecuencia de corte del limite inferior pues el superior
    # no afecta en nada
ind_f1 = int(ind_f1_c[0]) + ind_f_corte_inf
ind_f2 = int(ind_f2_c[0]) + ind_f_corte_inf
dbf1 = amplitud_fft_db[ind_f1] 
dbf2 = amplitud_fft_db[ind_f2]
f1 = vfreqpos[ind_f1]
f2 = vfreqpos[ind_f2]
f_DPOAE_teorica = 2*f1 - f2 
dbf1 = amplitud_fft_db[ind_f1]
dbf2 = amplitud_fft_db[ind_f2] 
f_DPOAE_teorica_ = round(f_DPOAE_teorica,1)
f_max, f_DPOAE_exp = localizar_maximo_entre([f_DPOAE_teorica_-0.2 , f_DPOAE_teorica_ +0.2],vfreqpos,amplitud_fft_db)
print("\n\n")
print("------------------------------------------------------")
print("    Resultados: ")
print(f"   * F1 = {f1} Hz ")
print(f"   * Amplitud F1 = {dbf1} dB_spl")
print(f"   * F2 = {f2} Hz ")
print(f"   * Amplitud F1 = {dbf2} dB_spl")
print(f"   * F_DPOAE_Teorica = {f_DPOAE_teorica} Hz")
print(f"   * F_DPOAE_exp = {f_max} Hz ")
print(f"   * Amplitud f_DPOAE_exp {f_DPOAE_exp} dB_SPL")
print("------------------------------------------------------")

print(" -- Graficando espectro -- ")
print("\n -- Cerrar la grafica para continuar -- ")
# Graficamos el espectro 
plt.stem(vfreqpos,amplitud_fft_db)
plt.title(nombre)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud [dB_spl]")
plt.show()