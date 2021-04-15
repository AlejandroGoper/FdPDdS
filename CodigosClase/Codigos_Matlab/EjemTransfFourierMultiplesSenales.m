close all;
clear variables;
%---------------parametros del muestreo de los datos-----------------------
% Es crucial saber el periodo de muestreo o la frecuenca de muestreo (el
% inverso del periodo)
Tmuestreo=0.001;
%Tiempo en el que se grabaron los datos (note que se quita un deltat porque
%la primera medici?n sucedi? en t=0 no en t=deltat)
TGrabacion=1; %unidades en segundos del tiempo de grabacion
tmax=TGrabacion-Tmuestreo;
%Se forma un vector con la variable independiente (en este caso t)
t=0:Tmuestreo:tmax; %es un vector que va de 0 a tmax en incrementos de deltat
%-------------parametros de la se?al a analizar----------------------------
%ahora se genera la se?al que es la suma de dos cosenos:
frecSenal1=1; %hz
frecSenal2=1.1; %hz
%amplitud de la primera senal:
A1=2;
%amplitud de la segunda senal:
A2=2.5;

senal=A1*cos(2*pi*frecSenal1*t)+A2*cos(2*pi*frecSenal2*t)+1.5;
%graficando la senal:
figure();
plot(t,senal);
title('Senal original');
axis on;
xlabel('t en seg');
ylabel('volts');
%calculando la transformada de Fourier
FFTsenal=fft(senal);
AmplitudFFT=CalculaVerdaderaAmplitud(FFTsenal);
%calculando el vector de frecuencias:
vfrec=CalcVectFrec(senal,Tmuestreo);
figure();
plot(fftshift(vfrec),abs(fftshift(FFTsenal)));
title ('Modulo de la transformada de Fourier de la senal'); 
xlabel('Frecuencia en Hz');
ylabel('|FFT|');
figure();
vfrecpos=vfrec(1:floor(size(senal,2)/2));
plot(vfrecpos,AmplitudFFT);
title ('Modulo de la transformada del abs(frec)'); 
xlabel('Frecuencia en Hz');
ylabel('|FFT|');