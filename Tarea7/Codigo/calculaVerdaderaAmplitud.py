"""
    Por I. Alejandro Gómez Pérez.
    
    La lógica de esta función es la siguiente:
    Toma unicamente los valores positivos de la fft (indices desde 0 hasta int(n/2)-1 [si n es par] 
    o desde 0 hasta int(n/2) [si n es impar]) duplica los valores de todo este arreglo (para así
    tomar en cuenta los valores negativos de las frecuencias) y finalmente dividimos entre el numero
    total de datos de la fft para encontrar así el valor de la amplitud correcta.
    
    ** Para construir el vector se uso una propiedad llamada slicing de los arreglos de python.

    Parámetros:
    fft: array que contiene la fft de alguna señal

    Regresa:
    vector: array con las contribuciones positivas de la fft con sus amplitudes correctas
"""
from numpy import floor,abs

def calculaVerdaderaAmplitud(fft):
    n = len(fft)
    if(n%2 == 0):
        lim = floor(n/2)
    else:
        lim = floor(n/2)+1
    vector = 2*abs(fft[0:int(lim)])/n
    vector[0] /= 2
    return vector