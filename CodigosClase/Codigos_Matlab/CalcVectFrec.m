function [ vfrec ] = CalcVectFrec( datos, PeriodoMuest )

%Esta funcion calcula el vector de los valores de la frecuencia (en Hz) en el
%espacio de Fourier de una secuencia guardada en el vector datos,
%PeriodoMuest, es el tiempo transcurrido entre medici?n y medici?n
N=size(datos,2);
%se calcula el valor en hertz de la frecuencia m?s baja de una onda que estar?a 
%completa en el vector de datos que se analiza, vean que el TiempoCompleto se
%calcula como el numero de muestras por el tiempo entre muestras
TiempoCompleto=PeriodoMuest*N;
if mod(N,2)==0
    %si las mediciones son pares se aparta un lugar entre los positivos
    %para el 0, la frec absoluta m?s alta se encontrar? en la secci?n de
    %las frec negativas y sera el n?mero de muestras N dividido entre 2,
    %esto se debe al teorema del muestreo que dice que la frecuancia m?s
    %alta que se puede observar es la mitad de la frecuencia de muestreo.
    vfrec=-floor(N/2):1:floor(N/2)-1;
else
    %si el numero de muestras es impar, entionces hay lugar para el 0
    vfrec=-floor(N/2):1:floor(N/2);
end
%Hasta la l?nea anterior las unidades de la frecuencia son repeticiones por 
%el tiempo completo de medici?n, para convertirlas en hertz (repeticiones 
%por segundo) hay que dividir entre el tiempo completo 
vfrec=ifftshift(vfrec)/TiempoCompleto;
%ahora si las unidades de frecuencia est?n en hertz, recuerde que el
%significado del signo menos en la frecuencia es un simplce cambio de fase.
end

