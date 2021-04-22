#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:08:48 2021

@author: alejandro_goper
"""
from numpy import where

"""
    Localiza el valor máximo de frecuencia en la senal, en un intervalo específico
    
    Parámetros:
        rango_frec: Lista con el intervalo de frecuencias donde se buscara el máximo
        vfrec: vector de frecuencias del cual hemos seleccionado el intervalo
        senal: la señal donde evaluaremos el punto con maxima frecuencia.
    Regresa:
        frec: Valor máximo de la frecuencia
        dato_maximo: Valor máximo en la senal
         
"""

def localizar_maximo_entre(rango_freq,vfrec,senal):
    # Encontramos los limites inferior y superior del intervalo
    lim_inf = rango_freq[0]
    lim_sup = rango_freq[1]
    # Encontramos los indices en el vector de frecuencias
    ind_lim_inf = where(vfrec == lim_inf)
    ind_lim_sup = where(vfrec == lim_sup)
    # convertimos a entero para poder realizar slicing
    ind_lim_inf = int(ind_lim_inf[0])
    ind_lim_sup = int(ind_lim_sup[0])
    # calculamos el indice del valor maximo en la senal unicamente en el intervalo deseado
    ind_maximo = where(senal[ind_lim_inf:ind_lim_sup] == max(senal[ind_lim_inf:ind_lim_sup]))
    # calculamos el indice real correspondiente añadiendo la contribución del limite inferior 
    ind_maximo = ind_maximo[0] + ind_lim_inf
    # evaluamos en la el vector frecuencia y la señal
    frec = vfrec[ind_maximo]
    dato_maximo = senal[ind_maximo]
    return frec,dato_maximo    