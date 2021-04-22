#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 02:16:59 2021

@author: alejandro_goper
"""
from numpy import where

"""
    Encuentra las dos frecuencias más dominantes en todo el intervalo de frecencias con base en su
    valor en la señal.
    
    
    Parametros:
        senal: espectro de amplitudes en la fft
        vfrecpos: vector de frecuencias
        tol: tolerancia dinamica
        
    Regresa:
        f_1 y f_2: Las dos frecuencias más notables en el espectro de la senal que satisfacen f_1 < f_2
        
    La lógica es: encontrar el máximo global, y realizar una partición con una tolerancia para evitar 
    que los puntos aledaños al valor global máximo afecten en la medición (dado que no es una delta 
                                                                           de Dirac perfecta)
    debemos asegurarnos que cuando busquemos la otra contribución más notable, no tomemos en cuenta 
    el intervalo [f_max-tol, f_max+tol] que es donde se encuentra todo el máximo global.
"""

#Bucando las frecuencias dominantes del espectro
def buscar_frecuencias(senal,vfrecpos,tol):
    #Buscando maximo globales
    indice_max_global = where(senal == senal.max())
    f_max_global = vfrecpos[indice_max_global]
    #Definiendo un rango de tolerancia para comenzar a buscar otro maximo 
    # Buscaremos despues de f_max_global + tol y antes de f_max_global - tol
    lim_sup_frec = f_max_global + tol
    lim_inf_frec = f_max_global - tol
    # Encontrando los indices del arrego de vfrecpos correspondientes a las frecuencias anteriores
    indice_lim_sup = where(vfrecpos == lim_sup_frec)
    indice_lim_inf = where(vfrecpos == lim_inf_frec)
    # Convirtiendo los valores a numeros enteros para poder realizar slicing
    indice_lim_sup = int(indice_lim_sup[0])
    indice_lim_inf = int(indice_lim_inf[0])
    # Encontramos el máximo de la región con indices 0:indice_lim_inf
    indice_max_inf = where(senal[:indice_lim_inf] == max(senal[:indice_lim_inf]))
    # y de la región con indices indice_lim_sup:end
    indice_max_sup = where(senal[indice_lim_sup:] == max(senal[indice_lim_sup:]))
    # note que a esta última región le tenemos que sumar el numero de indices recorridos ya
    indice_max_sup = indice_max_sup[0] + indice_lim_sup
    indice_max_inf = indice_max_inf[0]
    # Ahora decidiremos cual es el valor máximo entre las regiones inferior y superior establecidas
    # Encontramos el maximo relativo
    if(senal[indice_max_sup] > senal[indice_max_inf]):
        f_max_rel = vfrecpos[indice_max_sup]
    else:
        f_max_rel = vfrecpos[indice_max_inf]
    # Finalmente decidimos que frecuencia es mas alta y mas baja para encontrar asi f1 y f2
    if(f_max_global < f_max_rel):
        f_1 = f_max_global
        f_2 = f_max_rel
    else:
        f_1 = f_max_rel
        f_2 = f_max_global
    return f_1,f_2