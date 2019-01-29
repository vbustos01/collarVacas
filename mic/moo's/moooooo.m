% [y Fs] = audioread('cow-moo1.wav');
% % transformada de fourier
% Y = fftshift(fft(y));
% spec = (abs(Y)).^2;
% 
% figure
%     plot(spec)
%         grid minor
a = csvread('audio.txt')

figure
    plot(a)
        grid minor
