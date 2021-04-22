#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 23:12:50 2021

@author: I. Alejandro Gómez
"""

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

#Cargamos archivos

archivo = loadmat("../Archive/11_Datos.mat") #Dirección del archivo .mat
# Guardamos en arreglos numpy los datos de los archivos .mat
data = array(archivo["Data"]) # data es una matriz pero solo queremos un array
senal = data[0] # asi que solo tomamos la primera posicion
fs =  float(archivo["fs"]) # Convertimos a escalar float el dato del archivo

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

# Graficamos el espectro 
plt.stem(vfreqpos,amplitud_fft_db)
plt.title("11_Datos")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Db_SPL")

# Algoritmo principal

try:
    # Buscamos las dos frecuencias más prominentes en el espectro de Fourier
    f1,f2 = buscar_frecuencias(amplitud_fft_db,vfreqpos,10)
    # Obtenemos los índices en vfreqpos de estas frecuencias en específico
    # los necesitaremos para evaluar esa posición en el array de amplitud_fft_db
    ind_f1 = where(vfreqpos == f1)
    ind_f2 = where(vfreqpos == f2)
    # calculamos la f_DPOAE teórica
    f_DPOAE_teorica = 2*f1 - f2

    # Si esto se cumple quiere decir que se tomo un valor muy bajo de frecuencia
    # necesitamos eliminar el ruido de las frecuencias bajas
    # digamos que de 0 a 200 Hz es ruido, asi que 200 Hz es la frecuencia a la que 
    # cortaremos el espectro como vfreqpos[200:] y buscaremos de nuevo las frecuencias
    # sin tomar en cuenta esa parte del espectro

    while(f_DPOAE_teorica < 0):
        print("\nEl algoritmo encontro que F_DPOAE es negativa, lo cual viene por una mala elección de")
        print("las frecuencias F_1 y F_2. \n Para corregir esto debemos quitar el ruido de las primeras")
        print("partes del espectro.")
        frecuencia_corte = float(input("Ingrese un valor de frecuencia para cortar el espectro como valor:end : "))
        # Luego de ingresar la frecuencia, buscamos el indice en vfreqpos correspondiente
        ind_frec_corte = where(vfreqpos == frecuencia_corte)
        ind_frec_corte = int(ind_frec_corte[0])
        # Cortamos el espectro desde el indice anterior en adelante 
        # y calculamos nuevamente las frecuencias F1 y F2
        vfreqpos_cortada = vfreqpos[ind_frec_corte:]
        amplitud_fft_db_cortada = amplitud_fft_db[ind_frec_corte:]
        f1_c, f2_c = buscar_frecuencias(amplitud_fft_db_cortada, vfreqpos_cortada, 10)
        # Dado que ignoramos las frecuencias menores a frecuencia_corte 
        # a los indices de f1 y f2 obtenidos les falta la contribución del corte que hicimos 
        ind_f1_c = where(vfreqpos_cortada == f1_c)
        ind_f2_c = where(vfreqpos_cortada == f2_c)
        # Aqui añadimos la contribución a los índices de la frecuencia a partir de la cual cortamos
        ind_f1 = int(ind_f1_c[0]) + ind_frec_corte
        ind_f2 = int(ind_f2_c[0]) + ind_frec_corte
        # calculamos la F1 y F2 reales a partir de sus indices
        f1 = vfreqpos[ind_f1]
        f2 = vfreqpos[ind_f2]
        # calculamos nuevamente f_DPOAE_teorica, si es menor que 0 se repite el proceso con una
        # nueva frecuencia de corte
        f_DPOAE_teorica = 2*f1 - f2 
    
    # Al llegar a este punto, solo resta encontrar los decibelios correspondientes a las frecuencias
    # F1 y F2 encontradas 
    dbf1 = amplitud_fft_db[ind_f1]
    dbf2 = amplitud_fft_db[ind_f2] 
    print(f"Se encontraron:\n F1 = {f1} \t Db-SPL = {dbf1} \n F2 = {f2} \t Db-SPl = {dbf2}")
    print(f"F_DPOAE_Teorica = {f_DPOAE_teorica}")

    # Esta parte del programa encuentra de manera automatica la F_DPOAE experimental
    
    # Primero redondeamos a una cifra decimal el valor teorico obtenido
    # para que tenga tantas cifras significativas como el error permitido +- 0.2 Hz
    # con esto evitamos errores como por ejemplo que la frecuencia f_DPOAE +- 0.2 Hz no exista
    # en el espectro
    f_DPOAE_teorica_ = round(f_DPOAE_teorica,1)
    
    # Ahora, solo resta encontrar el valor máximo entre un intervalo específico de frecuencias
    # eso lo realizamos con la siguiente linea. 
    f_max, f_DPOAE_exp = localizar_maximo_entre([f_DPOAE_teorica_-0.2 , f_DPOAE_teorica_ +0.2],vfreqpos,amplitud_fft_db)
    print(f"f_DPOAE_exp = {f_max} \t dB_SPL f_DPOAE_exp {f_DPOAE_exp}\n")
    
except:
    # Si llegamos hasta aquí, ha ocurrido un error desconocido en el programa
    # probablemente tiene que ver con una mala elección de F1 y F2.
    
    # Así que, debemos encontrar un intervalo, menos conflictivos que el default (todo el espectro),
    # en donde creamos que se encuentren F1 y F2 y repetir el algoritmo pero ajustado ahora 
    # a solo buscar en el rango especificado de frecuencias.
    
    print("Se ha encontrado un error desconocido.\n")
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
    print(f"Se encontraron:\n F1 = {f1} \t Db-SPL = {dbf1} \n F2 = {f2} \t Db-SPl = {dbf2}")
    print(f"F_DPOAE_Teorica = {f_DPOAE_teorica}")
    f_DPOAE_teorica_ = round(f_DPOAE_teorica,1)
    f_max, f_DPOAE_exp = localizar_maximo_entre([f_DPOAE_teorica_-0.2 , f_DPOAE_teorica_ +0.2],vfreqpos,amplitud_fft_db)
    print(f"f_DPOAE_exp = {f_max} \t dB_SPL f_DPOAE_exp {f_DPOAE_exp}\n")