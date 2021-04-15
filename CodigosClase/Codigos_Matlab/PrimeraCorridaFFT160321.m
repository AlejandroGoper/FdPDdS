%cerrando ventanas viejas:
close all;
%ejemplos de llenado de valores de arreglos:
S1=[10i,9,8,7,6,5,4,3,2,1];
M1=[1+2i,2;3 4];
t=0:0.01:1;
t2=linspace(0,1,100);
%Comenzamos el programa para FFT
%Primero llenamos una secuencia con los valores de t en los que 
%queremos evaluar cos(t);
%DeltaT se refiere al tiempo que transcurre entre medicion y medicion
%Consideremos que esta en segundos
DeltaT=0.1;
%tiempo final
tf=2;
t=0:DeltaT:tf-DeltaT;
%f es la frecuencia de la se?al discretizada en ciclos/unidad de tiempo
%ciclos/segundo[=] Hertz
f=2;
%w es la frecuencia angular [=] rad/unidad de tiempo
%en este caso rad/segundo
w=2*pi*f;
%
f1=cos(w*t);
%grafica los valores de las secuencias pintando una curva suave
%entre puntos
plot(t,f1);
%pidiendo una nueva ventana para graficas
figure();
%graficando en forma de secuencia
stem(t,f1);
%Calculando la transformada de Fourier (Serie discreta de Fourier)
FF1=fft(f1);
figure();
%graficando la norma de la FFT
stem(abs(FF1));
title('|FF1|');
%graficando la fase de la FFT
figure();
stem(angle(FF1));
title('fase de FF1');
%las unidades de frecuencia est?n en ciclos por tiempo completo de medici?n